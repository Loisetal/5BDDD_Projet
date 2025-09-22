from pydantic import BaseModel
from datetime import datetime

class LoanCreate(BaseModel):
    user_id: int
    book_id: int

class LoanOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    loan_date: datetime
    return_date: datetime | None
    status: bool
    class Config:
        orm_mode = True
