from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean, Float
from sqlalchemy.orm import relationship
from db.base import Base

class StudentAnswer(Base):
    __tablename__ = 'student_answers2'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    question_paper_id = Column(Integer, ForeignKey('question_papers1.id'))
    total_questions = Column(Integer, default=0)
    given_ans_text = Column(String(255))
    given_ans_image = Column(String(255))
    is_correct = Column(Boolean, default=False) 
    wrong_answer= Column(Integer, default=0)
    #duration=Column(Integer, default=0)
    score = Column(Float)
    passed = Column(Boolean, default=False)
    
    
    
    users = relationship("LmsUsers", back_populates="answers")
    question_paper = relationship("QuestionPaper1", back_populates="student_answers")
    