# from sqlalchemy import Column, Integer, ForeignKey
# from sqlalchemy.orm import relationship
# from db.base import Base
# from .Questions import Question
# from .paper import Paper

# class QuestionMapping(Base):
#     __tablename__ = 'question_mapping'

#     mapping_id = Column(Integer, primary_key=True, index=True)
#     paper_id = Column(Integer, ForeignKey('papers.paper_id'))
#     question_id = Column(Integer, ForeignKey('questions.question_id'))

#     # Define relationships
#     question = relationship("Question", back_populates="mappings")
#     paper = relationship("Paper", back_populates="mappings")
    