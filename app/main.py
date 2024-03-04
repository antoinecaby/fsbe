
# System libs imports
from typing import Annotated
from datetime import timedelta, datetime, timezone

# Libs imports
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt

#local imports

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

ACCESS_TOKEN_EXPIRE_MINUTES= 60*24 # 24 hours
SECRET_KEY = "c60655a4fb84f0883c0ee1d2510eb332769029bc23ecd5796c53010ab01ba6f7"
ALGORITHM = "HS256"

users = [
    {   
        "id": 1,
        "email": "a@b.c",
        "name": "John",
        "age": 28,
        "birthPlace": "New York",
        "password": "1234"
    },
    {
        "id": 2,
        "email": "b@c.d",
        "name": "Jane",
        "age": 32,
        "password": "12345"
    },
    {
        "id": 3,
        "email": "c@d.e",
        "name": "Doe",
        "age": 45,
        "password": "123456"
    },
    {
        "id": 4,
        "email": "d@e.f",
        "name": "Smith",
        "password": "1234567",
        "age": 32,
    }
]

class CreateUser(BaseModel):
    name: str
    age: int | None = None
    email: str
    password: str

class User(CreateUser):
    id: int

class RootReturnObj(BaseModel):
    Hello: str


@app.post("/login")
async def login(credentials: Annotated[OAuth2PasswordRequestForm, Depends()]):
    for user in users:
        if user["email"] == credentials.username and user["password"] == credentials.password:


            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            jwt_creation_time = datetime.now(timezone.utc)
            expire = jwt_creation_time + access_token_expires
            to_encode = {
                "sub": credentials.username,
                "exp": expire,
                "iat": jwt_creation_time
            }
            
            encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
            return {"access_token": encoded_jwt, "token_type": "bearer"}
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

@app.get("/")
async def helloWorld() -> RootReturnObj:
    return {"Hello": "Worldazeazeaze"}


@app.get("/say-hello-john")
async def helloJohn(token: Annotated[str, Depends(oauth2_scheme)]):
    return "Hello John!"

# response_model_exclude_unset -> This remove the attributes that are not set in the response (= null or None)
@app.get("/users", response_model_exclude_unset=True)
async def getUsers(token: Annotated[str, Depends(oauth2_scheme)], minimum_age: int | None = None) -> list[User]:
    """
    Endpoint to return all users
    """
    print(token)
    if minimum_age:
        return [user for user in users if user["age"] >= minimum_age]
    return users

@app.get("/users/{user_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str}})
async def getUser(user_id: int) -> User:
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.post("/users", status_code=status.HTTP_201_CREATED, responses={status.HTTP_409_CONFLICT: {"model": str}})
async def createUser(user: CreateUser) -> User:
    max_id = 0
    for existing_user in users:
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email address already exists in the system.")
        if existing_user["id"] > max_id:
            max_id = existing_user["id"]

    # we made the checks before for the email, so we can be sure that the email is unique
    # we raise errors in that case and this piece of code won't be executed
    user = user.dict()
    user['id'] = max_id + 1
    users.append(user)
    return user

@app.delete("/users/{user_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str}})
async def deleteUser(user_id: int) -> None:
    for index, user in enumerate(users):
        if user["id"] == user_id:
            users.pop(index)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.put("/users/{user_id}", responses={status.HTTP_404_NOT_FOUND: {"model": str},
                                        status.HTTP_409_CONFLICT: {"model": str}})
async def updateUser(user_id: int, updated_user: CreateUser) -> None:
    user_index = None
    for index, user in enumerate(users):
        if user["email"] == updated_user.email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email address already exists in the system.")
        if user["id"] == user_id:
            user_index = index
    
    if user_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    updated_user = updated_user.dict()
    updated_user["id"] = user_id
    users[user_index]= updated_user
 