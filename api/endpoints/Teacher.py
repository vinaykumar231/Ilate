# from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from db.session import get_db
# from ..models.Teacher import Teacher as TeacherModel
# from pydantic import BaseModel, Field
# from ..schemas import TeacherCreate, TeacherResponse




# router = APIRouter()

# # ------------------------------------------------------------------------------------------------------------------
#                         #Teacher
# # ------------------------------------------------------------------------------------------------------------------

# # Create Teacher
# @router.post("/teachers/", response_model=TeacherResponse)
# def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
#     db_teacher = TeacherModel(**teacher.dict())
#     db.add(db_teacher)
#     db.commit()
#     db.refresh(db_teacher)
#     return db_teacher

# # Get Teacher by ID
# @router.get("/teachers/{teacher_id}", response_model=TeacherResponse)
# def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
#     db_teacher = db.query(TeacherModel).filter(TeacherModel.Teacher_id == teacher_id).first()
#     if db_teacher is None:
#         raise HTTPException(status_code=404, detail="Teacher not found")
#     return db_teacher

# # Update Teacher
# @router.put("/teachers/{teacher_id}", response_model=TeacherResponse)
# def update_teacher(teacher_id: int, teacher: TeacherCreate, db: Session = Depends(get_db)):
#     db_teacher = db.query(TeacherModel).filter(TeacherModel.Teacher_id == teacher_id).first()
#     if db_teacher is None:
#         raise HTTPException(status_code=404, detail="Teacher not found")
#     for key, value in teacher.dict().items():
#         setattr(db_teacher, key, value)
#     db.commit()
#     db.refresh(db_teacher)
#     return db_teacher

# # Delete Teacher
# @router.delete("/teachers/{teacher_id}")
# def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
#     db_teacher = db.query(TeacherModel).filter(TeacherModel.Teacher_id == teacher_id).first()
#     if db_teacher is None:
#         raise HTTPException(status_code=404, detail="Teacher not found")
#     db.delete(db_teacher)
#     db.commit()
#     return {"message": "Teacher deleted successfully"}
