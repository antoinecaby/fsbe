from typing import List
from fastapi import APIRouter, Depends, HTTPException,status
from sqlmodel import  Session
from model.models import User
from db.database import get_db
from Security.SecurityManager import SecurityManager
from model.schemas import UserCreate, UserLogin


router = APIRouter()
app=router

# Create a security manager instance
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


@app.post("/users/", response_model=User)
def add(user: UserCreate, db: Session = Depends(get_db)):
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
def update_user(user_id: int, user_update: UserCreate, session: Session = Depends(get_db)):
    """
    Update a user by ID.
    """
    # Retrieve the existing user from the database
    db_user = session.get(User, user_id)
    
    # Check if the user exists
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Encrypt the updated email, first name, and last name
    encrypted_email = security_manager.encrypt(user_update.email)
    encrypted_first_name = security_manager.encrypt(user_update.firstName)
    encrypted_last_name = security_manager.encrypt(user_update.lastName)
    
    # Hash the updated password
    hashed_password = security_manager.get_password_hash(user_update.password)
    
    # Update the user's attributes with the encrypted values and hashed password
    db_user.email = encrypted_email
    db_user.firstName = encrypted_first_name
    db_user.lastName = encrypted_last_name
    db_user.password = hashed_password
    
    # Commit the changes to the database and refresh the user object
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user



@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int, session: Session = Depends(get_db)):
    """
    Delete a user by ID.
    """
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return user



@router.post("/login/")
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """
    User login.
    """
    # Retrieve the user from the database based on the provided email
    all_users = db.query(User).all()
    for user in all_users:
        decrypted_email = security_manager.decrypt(user.email)
        if decrypted_email == user_login.email:
            # Verify the user's password
            if security_manager.verify_password(user_login.password, user.password):
                # Return a success message (this is where you would typically generate and return a token)
                return {"message": "Login successful"}
    
    # If user is not found or password is incorrect, raise an HTTPException
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
    )
