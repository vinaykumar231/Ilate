# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from db.base import Base

# class Paper(Base):
#     __tablename__ = 'papers'

#     paper_id = Column(Integer, primary_key=True)
#     title = Column(String(255))  # Corrected the declaration
#     description = Column(String(255))  # Corrected the declaration
#     user_id = Column(Integer, ForeignKey('users.user_id'))  

#     mappings = relationship("QuestionMapping", back_populates="paper")
