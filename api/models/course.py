from sqlalchemy import Column, Integer, String
from db.base import Base
from sqlalchemy.orm import relationship

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))

    #standards = relationship("Standard", back_populates="course")

    # subjects = relationship('Subject', back_populates='course')
    videos = relationship('Video', back_populates='course')
