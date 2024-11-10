from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime

def generate_id():
    return str(uuid4())

def generate_date():
    return str(datetime.now())

class User(BaseModel):
    id: str = Field(default_factory=generate_id)
    username: str
    email: str
    password: str
    created_at: str = Field(default_factory=generate_date)
    updated_at: str = Field(default_factory=generate_date)

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserDelete(BaseModel): 
    username: str
    password: str
    id: str
