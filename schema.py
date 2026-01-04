from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None 

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    # class Config:
    #     orm_mode = True # Enable ORM mode to work with SQLAlchemy models with Pydantic v1
    model_config = ConfigDict(from_attributes=True) # Enable ORM mode to work with SQLAlchemy models with Pydantic v2

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str