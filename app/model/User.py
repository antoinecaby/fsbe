from typing import List
from sqlmodel import SQLModel, Field, Relationship
from model.PlanningActivity import PlanningActivity

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str
    email: str
    password: str
    company_id: int
    company: "Company" = Relationship(back_populates="users")
    activities: "List[PlanningActivity]" = Relationship(back_populates="participants")

    @classmethod
    def get_user(cls, session, user_id: int):
        return session.query(cls).filter(cls.id == user_id).first()

    @classmethod
    def get_users_by_company(cls, session, company_id: int):
        return session.query(cls).filter(cls.company_id == company_id).all()
