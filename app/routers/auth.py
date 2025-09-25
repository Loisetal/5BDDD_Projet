from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.schemas.auth import LoginIn, Token

router = APIRouter(prefix="/auth", tags=["Authentification"])

@router.post("/enregistrement", response_model=UserOut, status_code=201,
             summary="Créer un nouvel utilisateur",
             description="Enregistre un nouvel utilisateur avec un nom, email, mot de passe et téléphone. L'email doit être unique.")
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    user = User(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        password=hash_password(payload.password),
        role=payload.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/connexion", response_model=Token,
             summary="Connexion utilisateur",
             description="Authentifie un utilisateur et retourne un token JWT pour les requêtes sécurisées.")
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants invalides")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return Token(access_token=token)
