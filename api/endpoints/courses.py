from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from ..models import Course, Subject, Standard, Module, Lesson
from ..schemas import CourseCreate, CourseUpdate
from auth.auth_bearer import JWTBearer, get_admin, get_teacher, get_admin_or_teacher
from pydantic import BaseModel,  Field
from typing import Optional, List
from fastapi import UploadFile, File
from datetime import date
from enum import Enum
from sqlalchemy import JSON


router = APIRouter()

##############################################################################################################################   
class CourseBase(BaseModel):
    name: str
    description: Optional[str]

class CourseCreate(CourseBase):
    pass

class StandardBase(BaseModel):
    name: str
    course_id: int

class StandardCreate(StandardBase):
    pass

class SubjectBase(BaseModel):
    name: str
    standard_id:int


class SubjectCreate(SubjectBase):
    pass

class ModuleBase(BaseModel):
    name: str
    subject_id:int

class ModuleCreate(ModuleBase):
    pass

class CourseCreateWithHierarchy(BaseModel):
    course: CourseCreate
    standards: List[StandardCreate]
    subjects: List[SubjectCreate]
    modules: List[ModuleCreate]
##############################################################################################################################

@router.post("/courses_create/", response_model=None)
def create_course_with_hierarchy(course_data: CourseCreateWithHierarchy, db: Session = Depends(get_db)):
    try:
        # Create course
        course = Course(name=course_data.course.name, description=course_data.course.description)
        db.add(course)
        db.commit()
        db.refresh(course)

        # Create standards
        for standard_data in course_data.standards:
            standard = Standard(name=standard_data.name, course_id=course.id)
            db.add(standard)

        # Create subjects
        for subject_data in course_data.subjects:
            subject = Subject(name=subject_data.name, standard_id=subject_data.standard_id)
            db.add(subject)

        # Create modules
        for module_data in course_data.modules:
            module = Module(name=module_data.name, subject_id=module_data.subject_id)
            db.add(module)

        db.commit()

        return {"message": "Course hierarchy created successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create course hierarchy: {str(e)}")

@router.get("/courses_hierarchy/{course_id}", response_model=CourseCreateWithHierarchy)
def get_course_hierarchy(course_id: int, db: Session = Depends(get_db)):
    try:
        # Retrieve the course
        course = db.query(Course).filter(Course.id == course_id).first()

        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        # Retrieve standards
        standards = db.query(Standard).filter(Standard.course_id == course_id).all()

        # Retrieve subjects
        subjects = []
        for standard in standards:
            subjects.extend(db.query(Subject).filter(Subject.standard_id == standard.id).all())

        # Retrieve modules
        modules = []
        for subject in subjects:
            modules.extend(db.query(Module).filter(Module.subject_id == subject.id).all())

        # Construct CourseCreateWithHierarchy object
        course_hierarchy = CourseCreateWithHierarchy(
            course={
                "name": course.name,
                "description": course.description
            },
            standards=[{
                "name": standard.name,
                "course_id": standard.course_id
            } for standard in standards],
            subjects=[{
                "name": subject.name,
                "standard_id": subject.standard_id
            } for subject in subjects],
            modules=[{
                "name": module.name,
                "subject_id": module.subject_id
            } for module in modules]
        )

        return course_hierarchy

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve course hierarchy: {str(e)}")

@router.delete("/courses_delete/{course_id}", response_model=None)
def delete_course_with_hierarchy(course_id: int, db: Session = Depends(get_db)):
    try:
        # Get the course
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        # Delete modules
        db.query(Module).filter(Module.subject_id.in_(db.query(Subject.id).filter(Subject.standard_id.in_(db.query(Standard.id)
                .filter(Standard.course_id == course_id))))).delete(synchronize_session=False)

        # Delete subjects
        db.query(Subject).filter(Subject.standard_id.in_(db.query(Standard.id).filter(Standard.course_id == course_id))).delete(synchronize_session=False)

        # Delete standards
        db.query(Standard).filter(Standard.course_id == course_id).delete(synchronize_session=False)

        # Delete course
        db.delete(course)
        db.commit()

        return {"message": "Course hierarchy deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete course hierarchy: {str(e)}")

    
##############################################################################################################################
@router.post("/courses/", response_model=None,
             dependencies=[Depends(JWTBearer()), Depends(get_admin)])
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    try:
        db_course = Course(**course.model_dump())
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        return db_course
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create course")


@router.get("/courses/", response_model=None)
def read_all_courses(db: Session = Depends(get_db)):
    try:
        return db.query(Course).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch courses")


@router.get("/courses/{course_id}", response_model=None)
def read_course(course_id: int, db: Session = Depends(get_db)):
    try:
        db_course = db.query(Course).filter(Course.id == course_id).first()
        if db_course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        return db_course
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch course")


@router.put("/courses/{course_id}", response_model=None,
            dependencies=[Depends(JWTBearer()), Depends(get_admin)])
def update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    try:
        db_course = db.query(Course).filter(Course.id == course_id).first()
        if db_course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        db_course.name = course.name
        db.commit()
        db.refresh(db_course)
        return db_course
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update course")


@router.delete("/courses/{course_id}", response_model=None,
               dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
def delete_course(course_id: int, db: Session = Depends(get_db)):
    try:
        db_course = db.query(Course).filter(Course.id == course_id).first()
        if db_course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        db.delete(db_course)
        db.commit()
        return db_course
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete course")
    

