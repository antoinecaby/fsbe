# model/models.py
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    firstName:str 
    lastName:str 
    email: str
    password: str
    company_id: Optional[int] = None  # Making company_id optional

    company_id: int = Field(foreign_key="company.id")  # Foreign key relationship with Company table
    isAdmin: bool   # New attribute to indicate if the user is an admin


    # Define the relationship between User and Company
    company: "Company" = Relationship(back_populates="users")

    # Define the many-to-many relationship between User and PlanningActivity
    activities: List["PlanningActivity"] = Relationship(back_populates="participant")
    
    # Define the relationship between User and Notification
    notifications: List["Notification"] = Relationship(back_populates="user")


class Company(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    address: str

    # Define the relationship between Company and User
    users: List[User] = Relationship(back_populates="company")


class Notification(SQLModel, table=True):
    id: int = Field(primary_key=True)
    message: str
    status: str
    user_id: int = Field(foreign_key="user.id")
    activity_id: int = Field(foreign_key="planningactivity.id")  # Add foreign key relationship

    # Define the relationship between Notification and User
    user: "User" = Relationship(back_populates="notifications")

    # Define the relationship between Notification and PlanningActivity
    activity: "PlanningActivity" = Relationship(back_populates="notifications")



class PlanningActivity(SQLModel, table=True):
    
    id: int = Field(primary_key=True)
    name: str
    day: str
    start_time: str
    end_time: str
    status: str = "unread"  
    user_id: int = Field(foreign_key="user.id")

    # Define the relationship between PlanningActivity and User
    participant: List[User] = Relationship(back_populates="activities")

    # Define the relationship between PlanningActivity and Notification
    notifications: List[Notification] = Relationship(back_populates="activity")
