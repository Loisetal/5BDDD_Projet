from sqlalchemy import Integer, TIMESTAMP, Boolean, ForeignKey, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Loan(Base):
    __tablename__ = "loan"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )
    book_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("book.id", ondelete="CASCADE"), nullable=False, index=True
    )
    loan_date: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
    return_date: Mapped[TIMESTAMP | None] = mapped_column(TIMESTAMP, nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")  # True=ongoing, False=returned

    user: Mapped["User"] = relationship("User", back_populates="loan")
    book: Mapped["Book"] = relationship("Book", back_populates="loan")

    __table_args__ = (
        Index("ix_loan_user_id", "user_id"),
        Index("ix_loan_book_id", "book_id"),
    )
