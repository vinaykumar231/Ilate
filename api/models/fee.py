from sqlalchemy import select, Column, Integer, String,ForeignKey, Float
from db.base import Base
from sqlalchemy.orm import Session, relationship
#from ..models import Course,Subject,Batch,Standard,Module


class Fee(Base):
    __tablename__ = "fees"

    id = Column(Integer, primary_key=True, index=True)
    course_id=Column(ForeignKey('courses.id'))
    standard_id=Column(ForeignKey('standards.id'))
    year=Column(Integer) # for xi, 1 year, for XI+XII: 2 year
    subject_id=Column(ForeignKey('subjects.id'))
    module_id=Column(ForeignKey('modules.id'))
    batch_id=Column(ForeignKey('batches.id'))
    amount=Column(Float) 

    # course = relationship("Course", back_populates="fees")
    # subject = relationship("Subject", back_populates="fees")
    # #batch = relationship("Batch", back_populates="fees")
    # standard = relationship("Standard", back_populates="fees")
    # module = relationship("Module", back_populates="fees")
    

   