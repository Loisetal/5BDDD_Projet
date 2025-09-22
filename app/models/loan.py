from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, Boolean, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    loan_date = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    return_date = Column(TIMESTAMP, nullable=True)
    status = Column(Boolean, nullable=False, server_default="true")  # True=ongoing, False=returned

    user = relationship("User")
    book = relationship("Book")
