from fastapi import FastAPI
from db.database import create_database
from routers import users_router, companies_router, notifications_router, activities_router
from sqlalchemy.orm import Session
from db.database import engine
from Security.SecurityManager import SecurityManager

# Dependency to get the database session
def get_session():
    with Session(engine) as session:
        yield session

# Dependency to get the database session
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

# Create a security manager instance
security_manager = SecurityManager()

create_database()
app = FastAPI()

app.include_router(users_router.router, prefix="/users", tags=["Users"])
app.include_router(companies_router.router, prefix="/companies", tags=["Companies"])
app.include_router(notifications_router.router, prefix="/notifications", tags=["Notifications"])
app.include_router(activities_router.router, prefix="/activities", tags=["Activities"])
