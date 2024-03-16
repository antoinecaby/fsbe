# model/schemas.py
from typing import List, Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    firstName:str 
    lastName:str 
    email: str
    password: str
    company_id: int
    isAdmin: bool = False    # New attribute to indicate if the user is an admin


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
    

class PlanningActivityUpdate(BaseModel):
    name: Optional[str]
    day: Optional[str]
    start_time: Optional[str]
    end_time: Optional[str]
    status: Optional[str] = "unread"  


class UserLogin(BaseModel):
    email: str
    password: str