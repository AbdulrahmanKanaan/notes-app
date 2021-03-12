from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from pydantic.networks import EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserCreate):
    id: int
    deleted_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
