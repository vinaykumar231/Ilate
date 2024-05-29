from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, func, TIMESTAMP
from sqlalchemy.orm import relationship
from db.base import Base
from .course import Course
from .standard import Standard
from .subject import Subject
from .module import Module
from .batch import Batch

class Payment(Base):
    __tablename__ = 'payments'

    payment_id = Column(Integer, primary_key=True , index= True)
    user_id = Column(Integer)
    course_id = Column(Integer, ForeignKey('courses.id'))
    standard_id = Column(Integer, ForeignKey('standards.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    module_id = Column(Integer, ForeignKey('modules.id'))
    batch_id = Column(Integer, ForeignKey('batches.id'))
    years = Column(Integer)
    amount = Column(Float)
    payment_mode = Column(String(255))
    payment_info = Column(String(255))
    other_info = Column(String(255))
    created_on = Column(DateTime, default=func.now())
    updated_on = Column(TIMESTAMP, server_default=None, onupdate=func.current_timestamp())


    # Establishing relationships
    #student = relationship("Student", back_populates="payments")
    course = relationship("Course", back_populates="payments")
    installments = relationship("Installment", back_populates="payment")
    #user = relationship("LmsUsers", back_populates="payments")

    course = relationship("Course", back_populates="payments")
    standard = relationship("Standard", back_populates="payments")
    subject = relationship("Subject", back_populates="payments")
    module = relationship("Module", back_populates="payments")
    batch = relationship("Batch", back_populates="payments")