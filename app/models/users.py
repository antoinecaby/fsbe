# libs import
from pydantic import BaseModel


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
        "password": "1234567"
    }
]

class CreateUser(BaseModel):
    name: str
    age: int | None = None
    email: str
    password: str

class User(CreateUser):
    id: int