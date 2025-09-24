from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user, require_role
from app.models.user import User
from app.models.loan import Loan
from app.schemas.user import UserOut, UserUpdate
from app.schemas.loan import LoanOut

router = APIRouter(prefix="/user", tags=["Utilisateur"], responses={401: {"description": "Non autorisé. Token invalide ou manquant"}})

@router.get("/{user_id}", response_model=UserOut,
            summary="Obtenir les informations d'un utilisateur",
            description="Retourne les informations de l'utilisateur dont l'ID est fourni.")
def read_user(user_id: int, db: Session = Depends(get_db), current=Depends(get_current_user), current_user: User = Depends(require_role(["admin"]))):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user


@router.patch("/{user_id}", response_model=UserOut,
              summary="Mettre à jour les informations d'un utilisateur",
              description=(
                  "Permet à l'utilisateur connecté de modifier certaines informations personnelles (nom, téléphone). "
                  "Les champs non fournis ne seront pas modifiés."
              ),
              response_description="Retourne les informations de l'utilisateur après mise à jour.")
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db), current=Depends(get_current_user), current_user: User = Depends(require_role(["admin"]))):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    if data.name is not None:
        user.name = data.name
    if data.phone is not None:
        user.phone = data.phone

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}/loans", response_model=list[LoanOut],
            summary="Lister les emprunts d'un utilisateur",
            description=(
                "Retourne l'historique des emprunts de l'utilisateur connecté, "
                "classés par date d'emprunt décroissante."
            ),
            response_description="Liste des emprunts effectués par l'utilisateur.")
def user_loans(user_id: int, db: Session = Depends(get_db), current=Depends(get_current_user)):
    if current.id != user_id and current.role != "admin":
        raise HTTPException(status_code=403, detail="Vous n'êtes pas autorisé à voir ces informations")

    loans = db.query(Loan).filter(Loan.user_id == user_id).order_by(Loan.loan_date.desc()).all()
    return loans


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT,
                summary="Supprimer un utilisateur",
                description="Supprime un utilisateur et tous ses emprunts associés. Seul l'utilisateur courant peut supprimer son compte.")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current=Depends(get_current_user),
    current_user: User = Depends(require_role(["admin"]))
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    db.query(Loan).filter(Loan.user_id == user_id).delete(synchronize_session=False)

    db.delete(user)
    db.commit()
    return None

