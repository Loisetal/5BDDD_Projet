from sqlalchemy import Column, Integer, String, Date, Boolean, TIMESTAMP, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.loan import Loan

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

    loans: Mapped[list["Loan"]] = relationship("Loan", back_populates="book")

    __table_args__ = (
        Index("ix_books_title", "title"),
        Index("ix_books_author", "author"),
        Index("ix_books_genre", "genre"),
    )