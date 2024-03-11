# internal/auth.py
from typing import Annotated, Optional
from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import func
from sqlmodel import Session
from Security.SecurityManager import SecurityManager
from db.database import get_db
from model.models import User

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
ACCESS_TOKEN_EXPIRE_MINUTES= 60*24 # 24 hours
ALGORITHM = "HS256"
SECRET_KEY = "4gN94qiDdlB3bnlYVeHBaIPTGPgOildOrxnrPaKYSQM="
security_manager = SecurityManager(SECRET_KEY)






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
    return {"access_token": encoded_jwt, "token_type": "bearer"}




async def get_decoded_token(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        print("Received token:", token)  # Print the received token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded payload:", payload)  # Print the decoded payload
        username = payload.get("sub")
        print("username = ",username)
        return payload
    except JWTError as e:
        print("JWTError occurred:", e)  # Print the JWTError exception
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"}) from e



def check_admin (token: str,db: Session) -> int:
        admin =0
        username = token["sub"]  # Access the 'sub' key directly from the token 
        all_users = db.query(User).all()
        for u in all_users:
         if security_manager.decrypt(u.email) == username:
             if u.isAdmin==True :
               admin =1
        print("admin= ",admin)
        return admin

    