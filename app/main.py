from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select
from database import create_database, get_session ,engine
from model.models import User, Company, Notification, PlanningActivity
from passlib.context import CryptContext

# Call create_database() to create the database tables
create_database()

app = FastAPI()

# Dependency to get the database session
def get_session():
    with Session(engine) as session:
        yield session

# CRUD operations for User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/users/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    """
    Create a new user.
    """
    hashed_password = pwd_context.hash(user.password)  # Hacher le mot de passe
    user.password = hashed_password  # Mettre à jour le mot de passe avec sa version hachée
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/users/", response_model=List[User])
def get_users(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    """
    Get all users.
    """
    users = session.exec(select(User).offset(skip).limit(limit)).all()
    return users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    """
    Get a specific user by ID.
    """
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User, session: Session = Depends(get_session)):
    """
    Update a user by ID.
    """
    db_user = session.get(User, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for var, value in vars(user).items():
        setattr(db_user, var, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    """
    Delete a user by ID.
    """
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return user

# CRUD operations for Company

@app.post("/companies/", response_model=Company)
def create_company(company: Company, session: Session = Depends(get_session)):
    """
    Create a new company.
    """
    session.add(company)
    session.commit()
    session.refresh(company)
    return company

@app.get("/companies/", response_model=List[Company])
def get_companies(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    """
    Get all companies.
    """
    companies = session.exec(select(Company).offset(skip).limit(limit)).all()
    return companies

@app.get("/companies/{company_id}", response_model=Company)
def get_company(company_id: int, session: Session = Depends(get_session)):
    """
    Get a specific company by ID.
    """
    company = session.get(Company, company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@app.put("/companies/{company_id}", response_model=Company)
def update_company(company_id: int, company: Company, session: Session = Depends(get_session)):
    """
    Update a company by ID.
    """
    db_company = session.get(Company, company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    for var, value in vars(company).items():
        setattr(db_company, var, value)
    session.add(db_company)
    session.commit()
    session.refresh(db_company)
    return db_company

@app.delete("/companies/{company_id}", response_model=Company)
def delete_company(company_id: int, session: Session = Depends(get_session)):
    """
    Delete a company by ID.
    """
    company = session.get(Company, company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    session.delete(company)
    session.commit()
    return company
# CRUD operations for Notification

@app.post("/notifications/", response_model=Notification)
def create_notification(notification: Notification, session: Session = Depends(get_session)):
    """
    Create a new notification.
    """
    session.add(notification)
    session.commit()
    session.refresh(notification)
    return notification

@app.get("/notifications/", response_model=List[Notification])
def get_notifications(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    """
    Get all notifications.
    """
    notifications = session.exec(select(Notification).offset(skip).limit(limit)).all()
    return notifications

@app.get("/notifications/{notification_id}", response_model=Notification)
def get_notification(notification_id: int, session: Session = Depends(get_session)):
    """
    Get a specific notification by ID.
    """
    notification = session.get(Notification, notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@app.put("/notifications/{notification_id}", response_model=Notification)
def update_notification(notification_id: int, notification: Notification, session: Session = Depends(get_session)):
    """
    Update a notification by ID.
    """
    db_notification = session.get(Notification, notification_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    for var, value in vars(notification).items():
        setattr(db_notification, var, value)
    session.add(db_notification)
    session.commit()
    session.refresh(db_notification)
    return db_notification

@app.delete("/notifications/{notification_id}", response_model=Notification)
def delete_notification(notification_id: int, session: Session = Depends(get_session)):
    """
    Delete a notification by ID.
    """
    notification = session.get(Notification, notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    session.delete(notification)
    session.commit()
    return notification


# CRUD operations for PlanningActivity

@app.post("/activities/", response_model=PlanningActivity)
def create_activity(activity: PlanningActivity, session: Session = Depends(get_session)):
    """
    Create a new planning activity.
    """
    session.add(activity)
    session.commit()
    session.refresh(activity)
    return activity

@app.get("/activities/", response_model=List[PlanningActivity])
def get_activities(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    """
    Get all planning activities.
    """
    activities = session.exec(select(PlanningActivity).offset(skip).limit(limit)).all()
    return activities

@app.get("/activities/{activity_id}", response_model=PlanningActivity)
def get_activity(activity_id: int, session: Session = Depends(get_session)):
    """
    Get a specific planning activity by ID.
    """
    activity = session.get(PlanningActivity, activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Planning Activity not found")
    return activity

@app.put("/activities/{activity_id}", response_model=PlanningActivity)
def update_activity(activity_id: int, activity: PlanningActivity, session: Session = Depends(get_session)):
    """
    Update a planning activity by ID.
    """
    db_activity = session.get(PlanningActivity, activity_id)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Planning Activity not found")
    for var, value in vars(activity).items():
        setattr(db_activity, var, value)
    session.add(db_activity)
    session.commit()
    session.refresh(db_activity)
    return db_activity

@app.delete("/activities/{activity_id}", response_model=PlanningActivity)
def delete_activity(activity_id: int, session: Session = Depends(get_session)):
    """
    Delete a planning activity by ID.
    """
    activity = session.get(PlanningActivity, activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Planning Activity not found")
    session.delete(activity)
    session.commit()
    return activity


