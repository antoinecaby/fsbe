# model/schemas.py
from typing import List, Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    company_id: int

class CompanyCreate(BaseModel):
    name: str
    address: str

class NotificationCreate(BaseModel):
    message: str
    status: str
    user_id: int
    activity_id: int

class PlanningActivityCreate(BaseModel):
    name: str
    day: str
    start_time: str
    end_time: str
    user_id: int
