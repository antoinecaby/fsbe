# model/Company.py
from typing import List
from sqlmodel import SQLModel, Field, Relationship

from .User import user  # Importing the User class using a relative import

class company(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    address: str

    # Define the relationship with User model
    users: List[user] = Relationship(back_populates="company")
