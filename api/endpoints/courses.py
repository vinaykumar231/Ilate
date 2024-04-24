from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from ..models import Course
from ..schemas import CourseCreate
from auth.auth_bearer import JWTBearer,get_admin, get_teacher, get_admin_or_teacher

router = APIRouter()


@router.post("/courses/", response_model=None,
             dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/courses/", response_model=None)
def read_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@router.get("/courses/{course_id}", response_model=None)
def read_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

@router.put("/courses/{course_id}", response_model=None,
            dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
def update_course(course_id: int, course: CourseCreate, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    db_course.name = course.name
    db_course.description = course.description
    db.commit()
    db.refresh(db_course)
    return db_course

@router.delete("/courses/{course_id}", response_model=None,
               dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(db_course)
    db.commit()
    return db_course
