from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlmodel import select
from database import get_session
from model.models import PlanningActivity
from schemas import PlanningActivityCreate

router = APIRouter()


class ActivitiesRouter:
    @router.post("/activities/", response_model=PlanningActivity)
    def create_activity(self, activity: PlanningActivityCreate, session: Session = Depends(get_session)):
        """
        Create a new planning activity.
        """
        # Implementation

    @router.get("/activities/", response_model=List[PlanningActivity])
    def get_activities(self, skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
        """
        Get all planning activities.
        """
        # Implementation

    @router.get("/activities/{activity_id}", response_model=PlanningActivity)
    def get_activity(self, activity_id: int, session: Session = Depends(get_session)):
        """
        Get a specific planning activity by ID.
        """
        # Implementation

    @router.put("/activities/{activity_id}", response_model=PlanningActivity)
    def update_activity(self, activity_id: int, activity_update: PlanningActivityCreate, session: Session = Depends(get_session)):
        """
        Update a planning activity by ID.
        """
        # Implementation

    @router.delete("/activities/{activity_id}", response_model=PlanningActivity)
    def delete_activity(self, activity_id: int, session: Session = Depends(get_session)):
        """
        Delete a planning activity by ID.
        """
        # Implementation
