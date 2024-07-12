from sqlalchemy import Column, Integer, String, ForeignKey
from db.base import Base
from sqlalchemy.orm import relationship

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True, index=True )
    name = Column(String(255))
    #course_id = Column(Integer, ForeignKey('courses.id'))
    standard_id = Column(Integer, ForeignKey("standards.id"))

    #course = relationship('Course', back_populates='subjects')
    standards = relationship("Standard", back_populates="subject")
    modules = relationship("Module", back_populates="subject")
    videos = relationship('Video', back_populates='subject')
    question_papers = relationship('QuestionPaper', back_populates='subject')

    course_details = relationship("CourseDetails", back_populates="subject")


    #fees = relationship("Fee", back_populates=" subject")
    payments = relationship("Payment", back_populates="subject")

    #student = relationship("Student",uselist=False, back_populates="subject")
    
    course_contents = relationship("Course_content", back_populates="subject")


