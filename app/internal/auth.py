# internal/auth.py
from typing import Annotated, Optional
from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session
from Security.SecurityManager import SecurityManager
from db.database import get_db
from model.models import User

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours
ALGORITHM = "HS256"
SECRET_KEY = "4gN94qiDdlB3bnlYVeHBaIPTGPgOildOrxnrPaKYSQM="
security_manager = SecurityManager(SECRET_KEY)

# Logged in users dictionary to store active tokens
logged_in_users = {}

# Logout endpoint
@router.post("/logout", tags=["auth"])
async def logout(token: str = Depends(oauth2_scheme)):
    """
    Invalidate the token by removing it from the logged_in_users dictionary.
    """
    try:
        payload = await get_decoded_token(token)  # Await get_decoded_token
        username = payload.get("sub")
        if username in logged_in_users:
            del logged_in_users[username]
        return {"message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Helper function to decode token
async def get_decoded_token(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Login endpoint
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    User login.
    """
    # Decrypt and compare the provided username with decrypted email in the database
    user = None
    all_users = db.query(User).all()
    for u in all_users:
        if security_manager.decrypt(u.email) == form_data.username:
            user = u
            break

    # Check if user exists, password is correct, and user is an admin
    if user is None or not security_manager.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    jwt_creation_time = datetime.now(timezone.utc)
    expire = jwt_creation_time + access_token_expires
    to_encode = {
        "sub": form_data.username,  # Using the decrypted email as the subject
        "exp": expire,
        "iat": jwt_creation_time
    }

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logged_in_users[form_data.username] = encoded_jwt  # Store the token for the logged-in user
    return {"access_token": encoded_jwt, "token_type": "bearer"}


def check_admin(token: str, db: Session) -> int:
    admin = 0
    username = token["sub"]  # Access the 'sub' key directly from the token
    all_users = db.query(User).all()
    for u in all_users:
        if security_manager.decrypt(u.email) == username:
            if u.isAdmin == True:
                admin = 1
    print("admin= ", admin)
    return admin


def check_company_access(token: str, company_id: int, db: Session) -> bool:
    """
    Check if the user associated with the token has access to the data of the specified company.
    """
    username = token["sub"]  # Access the 'sub' key directly from the token
    user_company_id = None
    all_users = db.query(User).all()
    for u in all_users:
        if security_manager.decrypt(u.email) == username:
            user_company_id = u.company_id
            print("user_company_id : ",user_company_id)
            break

    if user_company_id is None:
        return False
    
    # Check if the user's company ID matches the specified company ID
    return user_company_id == company_id