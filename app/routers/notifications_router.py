from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlmodel import select
from database import get_session
from model.models import Notification
from schemas import NotificationCreate

router = APIRouter()


class NotificationsRouter:
    @router.post("/notifications/", response_model=Notification)
    def create_notification(self, notification: NotificationCreate, session: Session = Depends(get_session)):
        """
        Create a new notification.
        """
        # Implementation

    @router.get("/notifications/", response_model=List[Notification])
    def get_notifications(self, skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
        """
        Get all notifications.
        """
        # Implementation

    @router.get("/notifications/{notification_id}", response_model=Notification)
    def get_notification(self, notification_id: int, session: Session = Depends(get_session)):
        """
        Get a specific notification by ID.
        """
        # Implementation

    @router.put("/notifications/{notification_id}", response_model=Notification)
    def update_notification(self, notification_id: int, notification_update: NotificationCreate, session: Session = Depends(get_session)):
        """
        Update a notification by ID.
        """
        # Implementation

    @router.delete("/notifications/{notification_id}", response_model=Notification)
    def delete_notification(self, notification_id: int, session: Session = Depends(get_session)):
        """
        Delete a notification by ID.
        """
        # Implementation
