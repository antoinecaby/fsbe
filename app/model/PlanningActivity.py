# PlanningActivity.py

from sqlmodel import SQLModel, Field, Relationship
from typing import List
from .User import User  # Import the User model

class PlanningActivity(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    day: str
    start_time: str
    end_time: str
    company_id: int

    # Define the relationship with User model
    participants: List[User] = Relationship(back_populates="activities")
