from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlmodel import select
from db.database import get_db, get_session
from internal.auth import get_decoded_token
from model.models import Notification, User
from model.schemas import NotificationCreate

router = APIRouter()

# CRUD operations for Notification

@router.post("/notifications", response_model=Notification)
def create_notification(notification: NotificationCreate,token: str = Depends(get_decoded_token), session: Session = Depends(get_db)):
    """
    Create a new notification.
    """
    db_notification = Notification(**notification.dict())
    session.add(db_notification)
    session.commit()
    session.refresh(db_notification)
    return db_notification

@router.get("/notifications", response_model=List[Notification])
def get_notifications(skip: int = 0, limit: int = 10,token: str = Depends(get_decoded_token), session: Session = Depends(get_db)):
    """
    Get all notifications.
    """
    notifications = session.query(Notification).offset(skip).limit(limit).all()
    return notifications

@router.get("/notifications/{notification_id}", response_model=Notification)
def get_notification(notification_id: int, token: str = Depends(get_decoded_token),session: Session = Depends(get_db)):
    """
    Get a specific notification by ID.
    """
    notification = session.get(Notification, notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.put("/notifications/{notification_id}", response_model=Notification)
def update_notification(notification_id: int, notification_update: NotificationCreate,token: str = Depends(get_decoded_token), session: Session = Depends(get_db)):
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
def delete_notification(notification_id: int, token: str = Depends(get_decoded_token),session: Session = Depends(get_db)):
    """
    Delete a notification by ID.
    """
    notification = session.get(Notification, notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    session.delete(notification)
    session.commit()
    return notification


@router.get("/users/{user_id}/notifications", response_model=List[Notification])
def get_user_notifications(user_id: int, token: str = Depends(get_decoded_token), session: Session = Depends(get_db)):
    """
    Get all notifications for a specific user.
    """
    # Retrieve the user
    user = session.query(User).filter(User.id == user_id).first()

    # Verify the user's existence
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Retrieve notifications for the user
    notifications = session.query(Notification).filter(Notification.user_id == user_id).all()
    return notifications






@router.put("/notifications/{notification_id}/unread", response_model=Notification)
def mark_notification_as_unread(notification_id: int, token: str = Depends(get_decoded_token), session: Session = Depends(get_db)):
    """
    Mark a notification as unread.
    """
    notification = session.get(Notification, notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")

    # Update the status to "unread"
    notification.status = "unread"
    session.commit()
    session.refresh(notification)
    return notification


@router.put("/notifications/{notification_id}/read", response_model=Notification)
def mark_notification_as_read(notification_id: int, token: str = Depends(get_decoded_token), session: Session = Depends(get_db)):
    """
    Mark a notification as read.
    """
    notification = session.get(Notification, notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")

    # Update the status to "unread"
    notification.status = "read"
    session.commit()
    session.refresh(notification)
    return notification
