from sqlalchemy import Column, Integer, String, Date, Boolean, TIMESTAMP, func, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
    author: Mapped[str] = mapped_column(String, nullable=False, index=True)
    genre: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    publication_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    available: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        Index("ix_books_title", "title"),
        Index("ix_books_author", "author"),
        Index("ix_books_genre", "genre"),
    )