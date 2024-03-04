from typing import List
from sqlmodel import SQLModel, Field, Relationship

class PlanningActivity(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    day: str
    start_time: str
    end_time: str
    company_id: int
    participants: "List[User]" = Relationship(back_populates="activities")

    @classmethod
    def get_activity(cls, session, activity_id: int):
        return session.query(cls).filter(cls.id == activity_id).first()

    @classmethod
    def get_activities_by_company(cls, session, company_id: int):
        return session.query(cls).filter(cls.company_id == company_id).all()
