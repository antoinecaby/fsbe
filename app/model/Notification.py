# model.Notification.py
from typing import List
from sqlmodel import SQLModel, Field

class notification(SQLModel, table=True):
    id: int = Field(primary_key=True)
    message: str
    status: str
    user_id: int
    activity_id: int

    @classmethod
    def get_notification(cls, session, notification_id: int):
        return session.query(cls).filter(cls.id == notification_id).first()

    @classmethod
    def get_notifications_by_user(cls, session, user_id: int):
        return session.query(cls).filter(cls.user_id == user_id).all()
