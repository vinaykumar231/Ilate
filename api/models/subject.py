from sqlalchemy import Column, Integer, String, ForeignKey
from db.base import Base
from sqlalchemy.orm import relationship

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    #course_id = Column(Integer, ForeignKey('courses.id'))
    #standard_id = Column(Integer, ForeignKey("standards.id"))

    #course = relationship('Course', back_populates='subjects')
    #standards = relationship("Standard", back_populates="subject")
    videos = relationship('Video', back_populates='subject')


