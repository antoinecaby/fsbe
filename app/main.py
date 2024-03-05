# main.py
from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select
from database import create_database , engine
from model.models import User, Company, Notification, PlanningActivity

# Call create_database() to create the database tables
create_database()

app = FastAPI()

# Dependency to get the database session
def get_session():
    with Session(engine) as session:
        yield session

# Endpoint to create a new user
@app.post("/users/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Endpoint to get all users
@app.get("/users/", response_model=List[User])
def get_users(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    users = session.exec(select(User).offset(skip).limit(limit)).all()
    return users

# Endpoint to create a new company
@app.post("/companies/", response_model=Company)
def create_company(company: Company, session: Session = Depends(get_session)):
    session.add(company)
    session.commit()
    session.refresh(company)
    return company

# Endpoint to get all companies
@app.get("/companies/", response_model=List[Company])
def get_companies(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    companies = session.exec(select(Company).offset(skip).limit(limit)).all()
    return companies

# Endpoint to create a new notification
@app.post("/notifications/", response_model=Notification)
def create_notification(notification: Notification, session: Session = Depends(get_session)):
    session.add(notification)
    session.commit()
    session.refresh(notification)
    return notification

# Endpoint to get all notifications
@app.get("/notifications/", response_model=List[Notification])
def get_notifications(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    notifications = session.exec(select(Notification).offset(skip).limit(limit)).all()
    return notifications

# Endpoint to create a new planning activity
@app.post("/activities/", response_model=PlanningActivity)
def create_activity(activity: PlanningActivity, session: Session = Depends(get_session)):
    session.add(activity)
    session.commit()
    session.refresh(activity)
    return activity

# Endpoint to get all planning activities
@app.get("/activities/", response_model=List[PlanningActivity])
def get_activities(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    activities = session.exec(select(PlanningActivity).offset(skip).limit(limit)).all()
    return activities
