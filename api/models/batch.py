from sqlalchemy import Column, Integer, String,ForeignKey
from db.base import Base
from sqlalchemy.orm import Session, relationship


class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)
    size= Column(String(223), nullable=False, unique=True)

    payments = relationship("Payment", back_populates="batch")