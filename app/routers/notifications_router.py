from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlmodel import select
from db.database import get_session
from model.models import Notification
from model.schemas import NotificationCreate

router = APIRouter()

# CRUD operations for Notification

@router.post("/notifications/", response_model=Notification)
def create_notification(notification: NotificationCreate, session: Session = Depends(get_session)):
    """
    Create a new notification.
    """
    db_notification = Notification(**notification.dict())
    session.add(db_notification)
    session.commit()
    session.refresh(db_notification)
    return db_notification

@router.get("/notifications/", response_model=List[Notification])
def get_notifications(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    """
    Get all notifications.
    """
    notifications = session.query(Notification).offset(skip).limit(limit).all()
    return notifications

@router.get("/notifications/{notification_id}", response_model=Notification)
def get_notification(notification_id: int, session: Session = Depends(get_session)):
    """
    Get a specific notification by ID.
    """
    notification = session.get(Notification, notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.put("/notifications/{notification_id}", response_model=Notification)
def update_notification(notification_id: int, notification_update: NotificationCreate, session: Session = Depends(get_session)):
    """
    Update a notification by ID.
    """
    db_notification = session.get(Notification, notification_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    for var, value in vars(notification_update).items():
        setattr(db_notification, var, value)
    session.add(db_notification)
    session.commit()
    session.refresh(db_notification)
    return db_notification

@router.delete("/notifications/{notification_id}", response_model=Notification)
def delete_notification(notification_id: int, session: Session = Depends(get_session)):
    """
    Delete a notification by ID.
    """
    notification = session.get(Notification, notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    session.delete(notification)
    session.commit()
    return notification
