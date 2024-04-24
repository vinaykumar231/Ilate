from sqlalchemy import Column, Integer, String, ForeignKey
from db.base import Base
from sqlalchemy.orm import relationship
class Standard(Base):
    __tablename__ = "standards"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    #course_id = Column(Integer, ForeignKey("courses.id"))

    #subject = relationship("Subject", back_populates="standards")
    videos = relationship('Video', back_populates='standard')
    #course = relationship("Course", back_populates="standards")
