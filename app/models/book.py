from sqlalchemy import Column, Integer, String, Date, Boolean, TIMESTAMP, func
from app.core.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False, index=True)
    genre = Column(String, nullable=True, index=True)
    publication_date = Column(Date, nullable=True)
    available = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
