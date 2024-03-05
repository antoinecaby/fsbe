# model/User.py
from typing import List
from sqlmodel import SQLModel, Field, Relationship

from Company import company  # Importing the Company class using a relative import

class user(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str
    email: str
    password: str
    company_id: int
    company: "company" = Relationship(back_populates="users")
    activities: "List[planning]" = Relationship(back_populates="participants")

    @classmethod
    def get_user(cls, session, user_id: int):
        return session.query(cls).filter(cls.id == user_id).first()

    @classmethod
    def get_users_by_company(cls, session, company_id: int):
        return session.query(cls).filter(cls.company_id == company_id).all()
