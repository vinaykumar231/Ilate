from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from pydantic import BaseModel, Field
from db.session import api_response, get_db, SessionLocal

from ..models.Test import Test
from ..models.module import Module
from .. models.module import Subject
from ..models.course import Course


router = APIRouter()


def create_test_paper(db, course_id: int, student_id: int, test_description: str):
    # Get course and related data
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Fetch any data you need from course, e.g., standards, subjects, modules, lessons
    standards = course.standards

    # You can continue fetching related data as needed
    # For example:
    for standard in standards:
        subjects = standard.subjects
        for subject in subjects:
            modules = subject.modules
            for module in modules:
                lessons = module.lessons
                # Now you have all lessons related to this module, you can use this data to create a test paper
    
    # Once you have the necessary data, create a test paper
    test = Test(description=test_description, teacher_id=1, student_id=student_id)
    db.add(test)
    db.commit()
    db.refresh(test)
    return test

# API endpoint to create a test paper
@router.post("/create_test_paper/")
def create_test_paper_endpoint(course_id: int, student_id: int, test_description: str):
    db = SessionLocal()
    try:
        test = create_test_paper(db, course_id, student_id, test_description)
        return test
    finally:
        db.close()
