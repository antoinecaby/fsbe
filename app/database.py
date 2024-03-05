from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

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
