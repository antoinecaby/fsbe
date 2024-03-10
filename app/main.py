# main.py
from fastapi import FastAPI
from db.database import create_database
from routers import users_router, companies_router, notifications_router, activities_router
from internal import auth


create_database()
app = FastAPI()

app.include_router(auth.router, tags=["auth"])
app.include_router(users_router.router, tags=["Users"])
app.include_router(companies_router.router, tags=["Companies"])
app.include_router(activities_router.router,tags=["Activities"])
app.include_router(notifications_router.router, tags=["Notifications"])
