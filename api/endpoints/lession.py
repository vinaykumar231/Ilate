# from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from db.session import get_db
# from ..models.lession import Lesson as LessonModel
# from pydantic import BaseModel, Field
# from ..schemas import LessonCreate, LessonResponse




# router = APIRouter()

# # ------------------------------------------------------------------------------------------------------------------
#                         #lession
# # ------------------------------------------------------------------------------------------------------------------

# # Create Lesson
# @router.post("/lessons/", response_model=LessonResponse)
# def create_lesson(lesson: LessonCreate, db: Session = Depends(get_db)):
#     db_lesson = LessonModel(**lesson.dict())
#     db.add(db_lesson)
#     db.commit()
#     db.refresh(db_lesson)
#     return db_lesson
# # Get Lesson by ID
# @router.get("/lessons/{lesson_id}", response_model=LessonResponse)
# def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
#     db_lesson = db.query(LessonModel).filter(LessonModel.lesson_id == lesson_id).first()
#     if db_lesson is None:
#         raise HTTPException(status_code=404, detail="Lesson not found")
#     return db_lesson

# # Update Lesson
# @router.put("/lessons/{lesson_id}", response_model=LessonResponse)
# def update_lesson(lesson_id: int, lesson: LessonCreate, db: Session = Depends(get_db)):
#     db_lesson = db.query(LessonModel).filter(LessonModel.lesson_id == lesson_id).first()
#     if db_lesson is None:
#         raise HTTPException(status_code=404, detail="Lesson not found")
#     for key, value in lesson.dict().items():
#         setattr(db_lesson, key, value)
#     db.commit()
#     db.refresh(db_lesson)
#     return db_lesson

# # Delete Lesson
# @router.delete("/lessons/{lesson_id}")
# def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
#     db_lesson = db.query(LessonModel).filter(LessonModel.lesson_id == lesson_id).first()
#     if db_lesson is None:
#         raise HTTPException(status_code=404, detail="Lesson not found")
#     db.delete(db_lesson)
#     db.commit()
#     return {"message": "Lesson deleted successfully"}
