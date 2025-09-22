from sqlalchemy import Integer, TIMESTAMP, Boolean, ForeignKey, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    book_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True
    )
    loan_date: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
    return_date: Mapped[TIMESTAMP | None] = mapped_column(TIMESTAMP, nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")  # True=ongoing, False=returned

    user: Mapped["User"] = relationship("User", back_populates="loans")
    book: Mapped["Book"] = relationship("Book", back_populates="loans")

    __table_args__ = (
        Index("ix_loans_user_id", "user_id"),
        Index("ix_loans_book_id", "book_id"),
    )
