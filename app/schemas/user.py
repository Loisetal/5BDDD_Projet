from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None

class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True
