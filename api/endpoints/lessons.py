from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from ..models import Lesson
from pydantic import BaseModel, Field
from ..schemas import LessonCreate, LessonResponse
from ..models.module import Module

router = APIRouter()

@router.post("/lessons/", response_model=None)
async def create_lesson(module_id: int, lesson: LessonCreate, db: Session = Depends(get_db)):
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    db_lesson = Lesson(**lesson.dict(), module_id=module_id)
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

@router.get("/lessons/get_all_lessons/", response_model=None)
async def read_lessons(db: Session = Depends(get_db)):
    lessons = db.query(Lesson).all()
    return lessons

@router.get("/lessons/{lesson_id}", response_model=LessonResponse)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    db_lesson = db.query(Lesson).filter(Lesson.lesson_id == lesson_id).first()
    if db_lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return db_lesson

@router.put("/lessons/{lesson_id}", response_model=None)
def update_lesson(lesson_id: int, lesson: LessonCreate, db: Session = Depends(get_db)):
    db_lesson = db.query(Lesson).filter(Lesson.lesson_id == lesson_id).first()
    if db_lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    for key, value in lesson.dict().items():
        setattr(db_lesson, key, value)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

@router.delete("/lessons/{lesson_id}")
def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    db_lesson = db.query(Lesson).filter(Lesson.lesson_id == lesson_id).first()
    if db_lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    db.delete(db_lesson)
    db.commit()
    return {"message": "Lesson deleted successfully"}