from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlmodel import select
from db.database import get_session
from model.models import PlanningActivity
from model.schemas import PlanningActivityCreate

router = APIRouter()

# CRUD operations for PlanningActivity

@router.post("/activities/", response_model=PlanningActivity)
def create_activity(activity: PlanningActivityCreate, session: Session = Depends(get_session)):
    """
    Create a new planning activity.
    """
    db_activity = PlanningActivity(**activity.dict())
    session.add(db_activity)
    session.commit()
    session.refresh(db_activity)
    return db_activity

@router.get("/activities/", response_model=List[PlanningActivity])
def get_activities(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    """
    Get all planning activities.
    """
    activities = session.query(PlanningActivity).offset(skip).limit(limit).all()
    return activities

@router.get("/activities/{activity_id}", response_model=PlanningActivity)
def get_activity(activity_id: int, session: Session = Depends(get_session)):
    """
    Get a specific planning activity by ID.
    """
    activity = session.get(PlanningActivity, activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Planning Activity not found")
    return activity

@router.put("/activities/{activity_id}", response_model=PlanningActivity)
def update_activity(activity_id: int, activity_update: PlanningActivityCreate, session: Session = Depends(get_session)):
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
def delete_activity(activity_id: int, session: Session = Depends(get_session)):
    """
    Delete a planning activity by ID.
    """
    activity = session.get(PlanningActivity, activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Planning Activity not found")
    session.delete(activity)
    session.commit()
    return activity
