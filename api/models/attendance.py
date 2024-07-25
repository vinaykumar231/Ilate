from sqlalchemy import Column, Integer, String, JSON, DateTime, func,Date, ForeignKey
from db.base import Base
from sqlalchemy.orm import relationship


class Attendance(Base):
    __tablename__ = "attendances1"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    date = Column(DateTime, default=func.now())
    status = Column(String(255), default="absent") 


    students = relationship("Student", back_populates="attendances")


    