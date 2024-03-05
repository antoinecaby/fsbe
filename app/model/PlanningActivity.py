# model.PlanningActivity.py
from sqlmodel import SQLModel, Field, Relationship
from typing import List


class planning(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    day: str
    start_time: str
    end_time: str
    company_id: int

    # Define the relationship with User model
    participants: List[user] = Relationship(back_populates="activities")
