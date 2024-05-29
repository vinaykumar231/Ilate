from sqlalchemy import Column, Integer, String,ForeignKey, JSON
from sqlalchemy.orm import relationship
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from db.base import Base
import shutil
import os
from pathlib import Path
import uuid

class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    lesson_id = Column(Integer, ForeignKey('lessons.lesson_id'))  # Corrected foreign key
    description = Column(String(255))
    content_type = Column(String(255))  
    content_path = Column(JSON) 

    lesson = relationship('Lesson', back_populates='content')
    

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