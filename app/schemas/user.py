from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.user import RoleEnum

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None

class UserCreate(UserBase):
    password: str
    role: RoleEnum = RoleEnum.user

class UserUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None

class UserOut(UserBase):
    id: int
    role: RoleEnum 
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True
