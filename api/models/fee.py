from sqlalchemy import select, Column, Integer, String,ForeignKey, Float
from db.base import Base
from sqlalchemy.orm import Session, relationship

class Fee(Base):
    __tablename__ = "fees"

    id = Column(Integer, primary_key=True, index=True)
    course_id=Column(ForeignKey('courses.id'))
    standard_id=Column(ForeignKey('standards.id'))
    year=Column(Integer) 
    subject_id=Column(ForeignKey('subjects.id'))
    module_id=Column(ForeignKey('modules.id'))
    batch_id=Column(ForeignKey('batches.id'))
    amount=Column(Float) 

    
    

   