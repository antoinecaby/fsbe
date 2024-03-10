from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db, get_session
from internal.auth import get_decoded_token
from model.models import PlanningActivity
from model.schemas import PlanningActivityCreate

router = APIRouter()

# CRUD operations for PlanningActivity

@router.post("/activities", response_model=PlanningActivity)
def create_activity(activity: PlanningActivityCreate, token: str = Depends(get_decoded_token),session: Session = Depends(get_db)):
    """
    Create a new planning activity.
    """
    db_activity = PlanningActivity(**activity.dict())
    session.add(db_activity)
    session.commit()
    session.refresh(db_activity)
    return db_activity

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

@router.put("/activities/{activity_id}", response_model=PlanningActivity)
def update_activity(activity_id: int, activity_update: PlanningActivityCreate, token: str = Depends(get_decoded_token),session: Session = Depends(get_db)):
    """
    Update a planning activity by ID.
    """
    db_activity = session.get(PlanningActivity, activity_id)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Planning Activity not found")
    for var, value in vars(activity_update).items():
        setattr(db_activity, var, value)
    session.add(db_activity)
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
