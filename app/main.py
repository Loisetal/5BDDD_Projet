
from fastapi import FastAPI, HTTPException
from app.routers import book, loan, auth, user

app = FastAPI(
    title="API Gestion Bibliothèque",
    description="Une API pour gérer les livres, les emprunts et les utilisateurs d'une bibliothèque.",
    version="1.0.0"
)

app.include_router(book.router)
app.include_router(loan.router)
app.include_router(auth.router)
app.include_router(user.router)

@app.get("/", summary="API Root")
async def root():
    return {"message": "API opérationnelle", "docs": "/docs"}

@app.exception_handler(NotImplementedError)
async def not_implemented_error_handler(request, exc):
    raise HTTPException(status_code=501, detail="Fonctionnalité non implémentée")
