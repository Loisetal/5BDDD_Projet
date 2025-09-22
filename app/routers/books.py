from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core import database
from app import models, schemas

router = APIRouter(prefix="/books", tags=["Books"], responses={404: {"description": "Livre non trouvé"}})

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/",
    response_model=List[schemas.BookOut],
    summary="Lister tous les livres",
    description="Récupère la liste complète des livres de la bibliothèque. "
                "Permet la pagination grâce aux paramètres `skip` et `limit`."
)
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Book).offset(skip).limit(limit).all()


@router.post(
    "/",
    response_model=schemas.BookOut,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un nouveau livre",
    description="Ajoute un nouveau livre dans la bibliothèque avec son titre, auteur, genre et autres informations."
)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get(
    "/{book_id}",
    response_model=schemas.BookOut,
    summary="Rechercher un livre avec son Id",
    description="Retourne les informations détaillées d’un livre à partir de son identifiant unique."
)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put(
    "/{book_id}",
    response_model=schemas.BookOut,
    summary="Mettre à jour un livre",
    description="Met à jour les informations d’un livre existant (titre, auteur, genre, etc.)."
)
def update_book(book_id: int, book_data: schemas.BookUpdate, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book_data.dict(exclude_unset=True).items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book


@router.patch(
    "/{book_id}",
    response_model=schemas.BookOut,
    summary="Modifier partiellement un livre",
    description="Met à jour uniquement certains champs d’un livre existant (par exemple seulement le titre ou la disponibilité)."
)
def patch_book(book_id: int, book_data: schemas.BookUpdate, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book_data.dict(exclude_unset=True).items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer un livre",
    description="Supprime un livre de la bibliothèque en fonction de son identifiant."
)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return None
