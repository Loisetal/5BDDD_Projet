from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.loan import Loan
from app.schemas.user import UserOut, UserUpdate
from app.schemas.loan import LoanOut

router = APIRouter(prefix="/user", tags=["Utilisateur"], responses={401: {"description": "Non autorisé. Token invalide ou manquant"}})

@router.get("/me", response_model=UserOut,
            summary="Obtenir les informations de l'utilisateur",
            description="Retourne les informations de l’utilisateur actuellement connecté.")
def read_me(current=Depends(get_current_user)):
    return current

@router.patch("/me", response_model=UserOut,
                summary="Mettre à jour les informations de l'utilisateur",
                description=(
                    "Permet à l’utilisateur connecté de modifier certaines informations personnelles (nom, téléphone). "
                    "Les champs non fournis ne seront pas modifiés."
                ),
                response_description="Retourne les informations de l’utilisateur après mise à jour."
            )
def update_me(data: UserUpdate, db: Session = Depends(get_db), current=Depends(get_current_user)):
    if data.name is not None:
        current.name = data.name
    if data.phone is not None:
        current.phone = data.phone
    db.add(current)
    db.commit()
    db.refresh(current)
    return current

@router.get("/me/loan", response_model=list[LoanOut],
            summary="Lister mes emprunts",
            description=(
                "Retourne l’historique des emprunts de l’utilisateur connecté, classés par date d’emprunt décroissante."
            ),
            response_description="Liste des emprunts effectués par l’utilisateur."
        )
def my_loans(db: Session = Depends(get_db), current=Depends(get_current_user)):
    loans = db.query(Loan).filter(Loan.user_id == current.id).order_by(Loan.loan_date.desc()).all()
    return loans
