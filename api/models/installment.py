# installment.py
from sqlalchemy import Column, Integer, Float, Date, ForeignKey,String,JSON
from sqlalchemy.orm import relationship
from db.base import Base

class Installment(Base):
    __tablename__ = 'installments'

    installment_id = Column(Integer, primary_key=True, autoincrement=True)
    payment_id = Column(Integer, ForeignKey('payments.payment_id'))
    total_amount = Column(Float)
    installment_number = Column(Integer)
    installments = Column(JSON) 

    payment = relationship("Payment", back_populates="installments")
