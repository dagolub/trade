from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = ""
    is_active: Optional[bool] = True
    is_superuser: bool = None
    full_name: Optional[str] = ""
    created: Optional[datetime]


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: Optional[str] = ""


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = ""


class UserInDBBase(UserBase):
    id: str
    _id: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
