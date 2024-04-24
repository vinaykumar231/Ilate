from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from ..models import Student
from ..schemas import StudentCreate, StudentUpdate

router = APIRouter()

# Get all students
@router.get("/students/", response_model=None)
async def read_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

# Get a specific student by ID
@router.get("/students/{student_id}", response_model=None)
async def read_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Create a new student
@router.post("/students/", response_model=None)
async def create_student(student_data: StudentCreate, db: Session = Depends(get_db)):
    student = Student(**student_data.dict())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

# Update a student by ID
@router.put("/students/{student_id}", response_model=None)
async def update_student(student_id: int, student_data: StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in student_data.dict().items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return student

# Delete a student by ID
@router.delete("/students/{student_id}", response_model=None)
async def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return student
