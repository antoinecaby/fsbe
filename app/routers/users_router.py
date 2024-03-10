# router/users_router;PY
from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from Security.SecurityManager import SecurityManager
from model.models import User
from model.schemas import UserCreate
from db.database import get_db
from internal.auth import get_decoded_token

router = APIRouter()
SECRET_KEY = "4gN94qiDdlB3bnlYVeHBaIPTGPgOildOrxnrPaKYSQM="
security_manager = SecurityManager(SECRET_KEY)


# Signup endpoint
@router.post("/signup/", response_model=User)
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


# Add user endpoint
@router.post("/users", response_model=User)
def add_user(user: UserCreate, token: str = Depends(get_decoded_token), db: Session = Depends(get_db)):
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


# Retrieve all users endpoint
@router.get("/users", response_model=List[User])
def get_users(token: str = Depends(get_decoded_token), skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
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


# Retrieve user by ID endpoint
@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, token: str = Depends(get_decoded_token), db: Session = Depends(get_db)):
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


# Update user by ID endpoint
@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserCreate, token: str = Depends(get_decoded_token), db: Session = Depends(get_db)):
    """
    Update a user by ID.
    """
    # Retrieve the existing user from the database
    db_user = db.query(User).filter(User.id == user_id).first()

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
    db.commit()
    db.refresh(db_user)

    return db_user


# Delete user by ID endpoint
@router.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int, token: str = Depends(get_decoded_token), db: Session = Depends(get_db)):
    """
    Delete a user by ID.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return user
