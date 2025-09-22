from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.loan import Loan
from app.schemas.user import UserOut, UserUpdate
from app.schemas.loan import LoanOut

router = APIRouter(prefix="/users", tags=["Utilisateurs"])

@router.get("/me", response_model=UserOut)
def read_me(current=Depends(get_current_user)):
    return current

@router.patch("/me", response_model=UserOut)
def update_me(data: UserUpdate, db: Session = Depends(get_db), current=Depends(get_current_user)):
    if data.name is not None:
        current.name = data.name
    if data.phone is not None:
        current.phone = data.phone
    db.add(current)
    db.commit()
    db.refresh(current)
    return current

@router.get("/me/loans", response_model=list[LoanOut])
def my_loans(db: Session = Depends(get_db), current=Depends(get_current_user)):
    loans = db.query(Loan).filter(Loan.user_id == current.id).order_by(Loan.loan_date.desc()).all()
    return loans
