from sqlalchemy import Column, Integer, String, ForeignKey
from db.base import Base
from sqlalchemy.orm import relationship
from .module import Module

class Lesson(Base):
    __tablename__ = 'lessons'

    lesson_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(String(255))
    module_id = Column(Integer, ForeignKey('modules.id'))  

    question_papers = relationship('QuestionPaper', back_populates='lesson')

    content = relationship('Content', back_populates='lesson')

    module = relationship('Module', back_populates='lessons')
    tests = relationship('Test', back_populates='lessons')
    

    