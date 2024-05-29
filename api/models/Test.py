from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base
from .Teacher import Teacher
from . Students import Student
from . lesson import Lesson
#from .Question_Paper_Table import QuestionPaper

class Test(Base):
    __tablename__ = 'tests'

    test_id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255))
    teacher_id = Column(Integer, ForeignKey('teachers.Teacher_id'))
    student_id = Column(Integer, ForeignKey('students.id'))
    lesson_id = Column(Integer, ForeignKey('lessons.lesson_id'))
    
    

    # Define relationships
    teacher = relationship("Teacher", back_populates="tests")
    student = relationship("Student", back_populates="tests")

    question = relationship("Question", back_populates="tests")
    question_paper = relationship("QuestionPaper", back_populates="tests")

    lessons = relationship('Lesson', back_populates='tests')


    
    