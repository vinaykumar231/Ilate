# from sqlalchemy import Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship
# from db.base import Base
# from .subject import Subject
# from .Teacher import Teacher
# from .Students import Student 
# from .module import Module
# from .lesson import Lesson
# from .Test import Test 


# class QuestionPaper(Base):
#     __tablename__ = 'question_papers_table'

#     id = Column(Integer, primary_key=True)
#     title = Column(String(255))
#     description = Column(String(255))
#     teacher_id = Column(Integer, ForeignKey('teachers.Teacher_id'))
#     student_id = Column(Integer, ForeignKey('students.id'))  # Updated field name to match the model
#     subject_id = Column(Integer, ForeignKey('subjects.id'))
#     module_id = Column(Integer, ForeignKey('modules.id'))
#     lesson_id = Column(Integer, ForeignKey('lessons.lesson_id'))
#     test_id = Column(Integer, ForeignKey('tests.test_id')) 
    
#     # subject = relationship("Subject", back_populates="question_papers")
#     #lesson = relationship("Lesson", back_populates="question_papers")
#     # teacher = relationship("Teacher", back_populates="question_papers")
#     # student = relationship("Student", back_populates="question_papers")
#     modules = relationship("Module", back_populates="question_papers")
#     tests = relationship("Test", back_populates="question_paper")

