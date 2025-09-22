
from fastapi import FastAPI
from app.routers import books

app = FastAPI(title="API Gestion Bibliothèque")

# Inclure les routes des livres
app.include_router(books.router)
