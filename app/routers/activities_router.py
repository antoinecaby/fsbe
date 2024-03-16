# router/activities_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db, get_session
from internal.auth import get_decoded_token
from model.models import Notification, PlanningActivity
from model.schemas import PlanningActivityCreate
from sqlalchemy.sql import text  # Import text from SQLAlchemy


router = APIRouter()


# CRUD operations for PlanningActivity


@router.post("/activities", response_model=PlanningActivity)
def create_activity(activity: PlanningActivityCreate, token: str = Depends(get_decoded_token), session: Session = Depends(get_db)):
    """
    Create a new planning activity.
    """
    try:
        # Insert the new activity into the database
        query = text("""
            INSERT INTO PlanningActivity (name, day, start_time, end_time, user_id, status)
            VALUES (:name, :day, :start_time, :end_time, :user_id, 'unmodified')
        """)
        session.execute(
            query,
            {
                "name": activity.name,
                "day": activity.day,
                "start_time": activity.start_time,
                "end_time": activity.end_time,
                "user_id": activity.user_id,
            }
        )
        session.commit()

        # Retrieve the ID of the newly inserted activity
        query = text("SELECT last_insert_rowid()")
        activity_id = session.execute(query).scalar()

        # Ensure activity.user_id is a list
        if not isinstance(activity.user_id, list):
            activity.user_id = [activity.user_id]

        # Generate notifications for users of this activity
        query = text("""
            INSERT INTO Notification (message, status, user_id, activity_id)
            VALUES (:message, :status, :user_id, :activity_id)
        """)
        for user_id in activity.user_id:
            session.execute(
                query,
                {
                    "message": f"New activity '{activity.name}' has been created.",
                    "status": "unread",
                    "user_id": user_id,
                    "activity_id": activity_id,
                }
            )
        session.commit()

        return {"id": activity_id, **activity.dict()}
    except Exception as e:
        # Rollback the transaction if an error occurs
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))





@router.get("/activities", response_model=List[PlanningActivity])
def get_activities(skip: int = 0, limit: int = 10,token: str = Depends(get_decoded_token), session: Session = Depends(get_db)):
    """
    Get all planning activities.
    """
    activities = session.query(PlanningActivity).offset(skip).limit(limit).all()
    return activities

@router.get("/activities/{activity_id}", response_model=PlanningActivity)
def get_activity(activity_id: int,token: str = Depends(get_decoded_token), session: Session = Depends(get_db)):
    """
    Get a specific planning activity by ID.
    """
    activity = session.get(PlanningActivity, activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Planning Activity not found")
    return activity

from model.schemas import PlanningActivityUpdate

@router.put("/activities/{activity_id}", response_model=PlanningActivity)
def update_activity(activity_id: int, activity_update: PlanningActivityUpdate, token: str = Depends(get_decoded_token),
                      session: Session = Depends(get_db)):
    """
    Update a planning activity by ID.
    """
    db_activity = session.query(PlanningActivity).filter(PlanningActivity.id == activity_id).first()
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Planning Activity not found")
    
    # Get the previous status of the activity
    previous_status = db_activity.status

    # Update the activity fields
    for field, value in activity_update.dict(exclude_unset=True).items():
        setattr(db_activity, field, value)
    
    # Generate notifications for users of the modified activity
    if "status" in activity_update.dict() and activity_update.status != previous_status:
        # Mark notifications as "unread" for users associated with the activity
        for user in db_activity.participant:
            notification = Notification(
                message=f"Activity '{db_activity.name}' has been updated.",
                status="unread",  # Set notification status as unread
                user_id=user.id,
                activity_id=db_activity.id
            )
            session.add(notification)
    
    session.commit()
    session.refresh(db_activity)
    return db_activity

@router.delete("/activities/{activity_id}", response_model=PlanningActivity)
def delete_activity(activity_id: int,token: str = Depends(get_decoded_token), session: Session = Depends(get_db)):
    """
    Delete a planning activity by ID.
    """
    activity = session.get(PlanningActivity, activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Planning Activity not found")
    session.delete(activity)
    session.commit()
    return activity


