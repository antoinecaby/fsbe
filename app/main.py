# main.py
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select
from Security.SecurityManager import SecurityManager
from database import create_database, get_session ,engine
from model.models import User, Company, Notification, PlanningActivity
from schemas import CompanyCreate, NotificationCreate, PlanningActivityCreate, UserCreate, UserLogin

# Call create_database() to create the database tables
create_database()

app = FastAPI()

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
security_manager = SecurityManager()


# Signup endpoint
@app.post("/signup/", response_model=User)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    # Hash the password
    hashed_password = security_manager.get_password_hash(user.password)
    
    # Encrypt the email, first name, and last name
    encrypted_email = security_manager.encrypt(user.email)
    encrypted_first_name = security_manager.encrypt(user.firstName)
    encrypted_last_name = security_manager.encrypt(user.lastName)
    
    # Create the User object with encrypted fields
    db_user = User(
        firstName=encrypted_first_name, 
        lastName=encrypted_last_name, 
        email=encrypted_email,
        password=hashed_password,
        company_id=user.company_id
    )
    
    # Save the user to the database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# ADD user endpoint

@app.post("/users/", response_model=User)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    # Hash the password
    hashed_password = security_manager.get_password_hash(user.password)
    
    # Encrypt the email, first name, and last name
    encrypted_email = security_manager.encrypt(user.email)
    encrypted_first_name = security_manager.encrypt(user.firstName)
    encrypted_last_name = security_manager.encrypt(user.lastName)
    
    # Create the User object with encrypted fields
    db_user = User(
        firstName=encrypted_first_name, 
        lastName=encrypted_last_name, 
        email=encrypted_email,
        password=hashed_password,
        company_id=user.company_id
    )
    
    # Save the user to the database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


# Login endpoint
@app.post("/login/")
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """
    User login.
    """
    # Retrieve the user from the database based on the provided email
    db_user = db.query(User).filter(User.email == user_login.email).first()
    
    # Verify the user's existence and password
    if not db_user or not security_manager.verify_password(user_login.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    # Return a success message (this is where you would typically generate and return a token)
    return {"message": "Login successful"}

# Endpoint to retrieve all users
@app.get("/users/", response_model=List[User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Get all users.
    """
    # Retrieve users from the database
    users = db.query(User).offset(skip).limit(limit).all()
    
    # Decrypt email, first name, and last name for each user
    for user in users:
        user.email = security_manager.decrypt(user.email)
        user.firstName = security_manager.decrypt(user.firstName)
        user.lastName = security_manager.decrypt(user.lastName)
    
    return users
# Endpoint to retrieve a user by ID
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a specific user by ID.
    """
    # Retrieve the user from the database based on the provided ID
    user = db.query(User).filter(User.id == user_id).first()
    
    # Verify the user's existence
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Decrypt email, first name, and last name for the user
    user.email = security_manager.decrypt(user.email)
    user.firstName = security_manager.decrypt(user.firstName)
    user.lastName = security_manager.decrypt(user.lastName)
    
    return user




@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserCreate, session: Session = Depends(get_session)):
    """
    Update a user by ID.
    """
    db_user = session.get(User, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for var, value in vars(user_update).items():
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
# main.py

# CRUD operations for Company

@app.post("/companies/", response_model=Company)
def create_company(company: CompanyCreate, session: Session = Depends(get_session)):
    """
    Create a new company.
    """
    db_company = Company(**company.dict())
    session.add(db_company)
    session.commit()
    session.refresh(db_company)
    return db_company

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
def update_company(company_id: int, company_update: CompanyCreate, session: Session = Depends(get_session)):
    """
    Update a company by ID.
    """
    db_company = session.get(Company, company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    for var, value in vars(company_update).items():
        setattr(db_company, var, value)
    session.add(db_company)
    session.commit()
    session.refresh(db_company)
    return db_company

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
def create_notification(notification: NotificationCreate, session: Session = Depends(get_session)):
    """
    Create a new notification.
    """
    db_notification = Notification(**notification.dict())
    session.add(db_notification)
    session.commit()
    session.refresh(db_notification)
    return db_notification

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
def update_notification(notification_id: int, notification_update: NotificationCreate, session: Session = Depends(get_session)):
    """
    Update a notification by ID.
    """
    db_notification = session.get(Notification, notification_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    for var, value in vars(notification_update).items():
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
def create_activity(activity: PlanningActivityCreate, session: Session = Depends(get_session)):
    """
    Create a new planning activity.
    """
    db_activity = PlanningActivity(**activity.dict())
    session.add(db_activity)
    session.commit()
    session.refresh(db_activity)
    return db_activity

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
def update_activity(activity_id: int, activity_update: PlanningActivityCreate, session: Session = Depends(get_session)):
    """
    Update a planning activity by ID.
    """
    db_activity = session.get(PlanningActivity, activity_id)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Planning Activity not found")
    for var, value in vars(activity_update).items():
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
