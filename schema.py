from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, conint
from typing import Annotated, Optional

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
    owner_id: int
    owner: UserOut

    # class Config:
    #     orm_mode = True # Enable ORM mode to work with SQLAlchemy models with Pydantic v1
    model_config = ConfigDict(from_attributes=True) # Enable ORM mode to work with SQLAlchemy models with Pydantic v2

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None # Optional field to handle cases where token might not have id why did he use str before?

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]  # 1 = upvote, 0 = remove
    # dir : conint(le=1)  # 1 for upvote, 0 for remove vote