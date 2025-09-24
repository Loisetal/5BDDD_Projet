from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.models.user import User
from app.core.deps import require_role

from app.core import database
from app import models, schemas

router = APIRouter(prefix="/loan", tags=["Loan"], responses={404: {"description": "Emprunt non trouvé"}})

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Lister tous les emprunts
@router.get(
    "/",
    response_model=List[schemas.LoanOut],
    summary="Lister tous les emprunts",
    description="Retourne la liste complète des emprunts effectués."
)
def read_loans(db: Session = Depends(get_db)):
    return db.query(models.Loan).all()

# Créer un emprunt
@router.post(
    "/",
    response_model=schemas.LoanOut,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un nouvel emprunt",
    description="Associe un utilisateur et un livre à un emprunt. Le livre devient ensuite indisponible.",
)
def create_loan(loan: schemas.LoanCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role(["user", "admin"]))):
    if current_user.role != "admin" and current_user.id != loan.user_id:
        raise HTTPException(
            status_code=403,
            detail="Vous ne pouvez créer un emprunt que pour vous-même"
        )
    
    book = db.query(models.Book).filter(models.Book.id == loan.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.available:
        raise HTTPException(status_code=400, detail="Book is not available")

    user = db.query(models.User).filter(models.User.id == loan.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Créer l'emprunt
    db_loan = models.Loan(
        user_id=loan.user_id,
        book_id=loan.book_id,
        loan_date=datetime.utcnow(),
        status=True
    )
    book.available = False
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

# Récupérer un emprunt par ID
@router.get(
    "/{loan_id}",
    response_model=schemas.LoanOut,
    summary="Récupérer un emprunt",
    description="Retourne les détails d’un emprunt spécifique."
)
def read_loan(loan_id: int, db: Session = Depends(get_db),  current_user: User = Depends(require_role(["user", "admin"]))):
    loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    if current_user.role != "admin" and loan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Accès refusé à cet emprunt")
    return loan

# Retourner un livre (clôturer un emprunt)
@router.put(
    "/{loan_id}/return",
    response_model=schemas.LoanOut,
    summary="Retourner un livre",
    description="Clôture un emprunt en définissant la date de retour et en rendant le livre disponible."
)
def return_book(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    if not loan.status:
        raise HTTPException(status_code=400, detail="Book already returned")

    # Mettre à jour l’emprunt
    loan.return_date = datetime.utcnow()
    loan.status = False

    # Rendre le livre dispo
    book = db.query(models.Book).filter(models.Book.id == loan.book_id).first()
    if book:
        book.available = True

    db.commit()
    db.refresh(loan)
    return loan
    