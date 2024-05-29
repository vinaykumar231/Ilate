from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import relationship
from db.base import Base
from .user import LmsUsers
import os
import shutil
import uuid
#from .payment import Payment

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    first_name = Column(String(255))
    middle_name = Column(String(255), nullable=True)
    last_name = Column(String(255))
    date_of_birth = Column(Date)
    gender = Column(String(255))
    nationality = Column(String(255))
    referral = Column(String(255))
    id_proof = Column(String(255))
    Address_proof = Column(String(255))  # Corrected column name
    date_of_joining = Column(Date)
    date_of_completion = Column(Date, nullable=True)
    #is_payment_done = Column(Boolean, server_default='0', nullable=False)
    #is_formsubmited= Column(Boolean, server_default='0', nullable=False)

    # Define one-to-one relationship with ContactInformation
    #contact_info = relationship("ContactInformation", uselist=False, back_populates="student")
    
    # Define one-to-many relationship with PreEducation
    pre_education = relationship("PreEducation", uselist=False,  back_populates="student")
    
    # Define one-to-one relationship with Parent
    parent_info = relationship("Parent", uselist=False, back_populates="student")
    
    # Define relationship with QuestionPaper
    question_papers = relationship('QuestionPaper', back_populates='student')
    
    # Define relationship with LmsUsers
    user = relationship("LmsUsers", back_populates="student")
    tests = relationship("Test", back_populates="student", overlaps="user")

    #payments = relationship("Payment", back_populates="student")

    contact_info = relationship("ContactInformation",uselist=False, back_populates="student")

    course_details = relationship("CourseDetails",uselist=False, back_populates="student")

    # #course = relationship("Course", back_populates="student")
    # subject = relationship("Subject",uselist=False, back_populates="student")
    # #module = relationship("Module",uselist=False, back_populates="student")
    # standard = relationship("Standard",uselist=False, back_populates="student")





def save_upload(upload_file: UploadFile) -> str:
    try:
        # Generate a unique filename using UUID
        unique_filename = str(uuid.uuid4()) + "_" + upload_file.filename
        file_path = os.path.join("uploads", unique_filename)

        # Save the file to the specified path
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        
        return file_path
    except Exception as e:
        # Handle file saving errors
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")