from typing import Optional
from pydantic import BaseModel, EmailStr
from models.user import UserStatus


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserStatus


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UserInDBBase(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str