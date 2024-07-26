from sqlalchemy import Column, Integer, ForeignKey,String, Text, DateTime,func
from sqlalchemy.orm import relationship
from db.base import Base
#from .Questions import Question1
# from .paper import Paper

class QuestionPaper1(Base):
    __tablename__ = 'question_papers1'

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey('lessons.lesson_id'))
    lesson_title = Column(String(255))
    created_on = Column(DateTime, default=func.now())
    created_by = Column(Integer, ForeignKey('teachers.Teacher_id'))

    lesson = relationship("Lesson", back_populates="question_papers")
    teacher = relationship("Teacher", back_populates="created_question_papers")
    questions = relationship("LessontestQuestion", back_populates="question_paper")
    student_answers = relationship("StudentAnswer", back_populates="question_paper")