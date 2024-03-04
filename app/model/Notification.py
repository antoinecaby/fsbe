# main.py

from fastapi import FastAPI
from sqlmodel import create_engine, Session
from app.model.Company import Company
from app.model.Notification import Notification
from app.model.PlanningActivity import PlanningActivity
from app.model.User import User

DATABASE_URL = "sqlite:///./fsbe.db"
engine = create_engine(DATABASE_URL)

def create_database():
    SQLModel.metadata.create_all(engine)

def main():
    create_database()

    with Session(engine) as session:
        # Add instances to the session
        user = User(username="John", email="john@example.com", password="password123", company_id=1)
        session.add(user)

        company = Company(name="ABC Inc.", address="123 Street")
        session.add(company)

        planning_activity = PlanningActivity(name="Meeting", day="2024-03-05", start_time="09:00", end_time="10:00", company_id=1)
        session.add(planning_activity)

        notification = Notification(message="Meeting rescheduled", status="unread", user_id=1, activity_id=1)
        session.add(notification)

        # Commit the session to save changes to the database
        session.commit()

app = FastAPI()

# Import the main function and call it when needed
from main import main

@app.get("/")
async def root():
    main()
    return {"message": "Data initialized successfully!"}
