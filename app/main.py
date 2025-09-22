
from fastapi import FastAPI
from app.routers import books, auth, users

app = FastAPI(title="API Gestion Bibliothèque")

# Inclure les routes des livres
app.include_router(books.router)
app.include_router(auth.router)
app.include_router(users.router)
# app.include_router(loans.router)
