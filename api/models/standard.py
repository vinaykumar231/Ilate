from sqlalchemy import Column, Integer, String, ForeignKey
from db.base import Base
from sqlalchemy.orm import relationship
class Standard(Base):
    __tablename__ = "standards"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    course_id = Column(Integer, ForeignKey("courses.id"))

    subject = relationship("Subject", back_populates="standards")
    videos = relationship('Video', back_populates='standard')
    course = relationship("Course", back_populates="standards")

    course_details = relationship("CourseDetails", back_populates="standard")
    #fees = relationship("Fee", back_populates="standard")
    

    payments = relationship("Payment", back_populates="standard")

    #student = relationship("Student",uselist=False, back_populates="standard")
