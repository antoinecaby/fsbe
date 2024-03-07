# database.py
from sqlalchemy import create_engine, inspect
from sqlmodel import SQLModel, Session
from model.models import User, Company, Notification, PlanningActivity

# Database URL for SQLite
DATABASE_URL = "sqlite:///./fsbe.db"

# Create the engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Function to create a new database session
def get_session():
    with Session(engine) as session:
        yield session

# Function to create the database tables
def create_database():
    SQLModel.metadata.create_all(engine)
    # Create tables for all SQLModel classes only if they don't already exist
    with engine.begin() as conn:
        inspector = inspect(engine)
        for model in [User, Company, Notification, PlanningActivity]:
            if not inspector.has_table(model.__tablename__):
                model.__table__.create(engine)
