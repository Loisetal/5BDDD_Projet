from pydantic import BaseModel
from datetime import date, datetime

class BookBase(BaseModel):
    title: str
    author: str
    genre: str | None = None
    publication_date: date | None = None

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    genre: str | None = None
    publication_date: date | None = None
    available: bool | None = None

class BookOut(BookBase):
    id: int
    available: bool
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True
