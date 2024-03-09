# internal/auth
from typing import Annotated
from datetime import timedelta, datetime, timezone

# Libs imports
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session
from Security.SecurityManager import SecurityManager
from db.database import get_db
from model.models import User
from passlib.context import CryptContext




security_manager = SecurityManager()



router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
ACCESS_TOKEN_EXPIRE_MINUTES= 60*24 # 24 hours
SECRET_KEY = "c60655a4fb84f0883c0ee1d2510eb332769029bc23ecd5796c53010ab01ba6f7"
ALGORITHM = "HS256"


async def get_decoded_token(token: str = Depends(oauth2_scheme)):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return(payload.get("sub"))
  except JWTError as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"}) from e


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    User login.
    """
    # Decrypt and compare the provided username with decrypted email in the database
    user = None
    all_users = db.query(User).all()
    for u in all_users:
        print(u)
        if SecurityManager.decrypt(u.email) == form_data.username:
            user = u
            break

    if user is None or not SecurityManager.verify_password(form_data.password, user.password):
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