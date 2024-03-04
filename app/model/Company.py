# Company.py

from sqlmodel import SQLModel, Field, Relationship
from typing import List
from .User import User  # Import the User model

class Company(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    address: str

    # Define the relationship with User model
    users: List[User] = Relationship(back_populates="company")
