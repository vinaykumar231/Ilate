from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.base import Base 

class CourseDetails(Base):
    __tablename__ = "course_details"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(255))
    standard = Column(String(255))
    module = Column(String(255))
    course = Column(String(255))
    student_id = Column(Integer, ForeignKey("students.id"))

    
    student = relationship("Student", back_populates="course_details")
