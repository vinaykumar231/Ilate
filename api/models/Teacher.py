from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base
from .user import LmsUsers

class Teacher(Base):
    __tablename__ = 'teachers'

    Teacher_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    name = Column(String(255))
    email = Column(String(255), unique=True)
    department = (String(255))
    
    question_papers = relationship('QuestionPaper', back_populates='teacher')
    tests = relationship('Test', back_populates='teacher')

    # Define one-to-one relationship with TeacherContact
    contact_information = relationship("TeacherContact", back_populates="teacher")
    
    educations = relationship("Education", back_populates="teacher")

    dependents = relationship("Dependents", back_populates="teacher")

    emergency_contact = relationship("EmergencyContact", back_populates="teacher")

    skills = relationship("Skill", back_populates="teacher")

    languages_spoken = relationship("LanguagesSpoken", back_populates="teacher")

    employee = relationship('Employee', back_populates='teacher')

    user = relationship("LmsUsers", back_populates="teacher")

    courses_by = relationship("TeacherCourse", back_populates="teacher_Assign")
