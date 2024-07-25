from fastapi import FastAPI, Depends, HTTPException,APIRouter
from datetime import datetime
from sqlalchemy.orm import Session
from db.session import get_db
from pydantic import BaseModel
from datetime import date
from typing import List
from enum import Enum
from ..models.attendance import Attendance
from ..models.user import LmsUsers
from ..schemas import AttendanceStatus, AttendanceCreate, AttendanceResponse
import pytz
from ..models import Student

router = APIRouter()


@router.post("/attendance/", response_model=None)
def create_attendance(student_id: int, attendance: AttendanceCreate, db: Session = Depends(get_db)):
    student_db= db.query(Student).filter(Student.id== student_id).first()
    if not student_db:
        raise HTTPException(status_code=404, detail="student not found")
    db_attendance = Attendance(**attendance.dict(), student_id= student_id)
    utc_now = pytz.utc.localize(datetime.utcnow())
    ist_now = utc_now.astimezone(pytz.timezone('Asia/Kolkata'))
    db_attendance.date = ist_now
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

@router.get("/attendance/{student_id}", response_model=List[AttendanceResponse])
def get_student_attendance(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    attendances = db.query(Attendance).filter(Attendance.student_id == student_id).all()
    
    if not attendances:
        return []
    
    student_name = f"{student.first_name} {student.last_name}"
    
    return [
        AttendanceResponse(
            id=attendance.id,
            student_id=student_id,
            student_name=student_name,
            student_attendance_status=attendance.status,
            date=attendance.date
        )
        for attendance in attendances
    ]
@router.get("/attendance_students/", response_model=None)
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students

@router.put("/attendance/{student_id}", response_model=AttendanceResponse)
def update_attendance(student_id: int, status: AttendanceStatus, db: Session = Depends(get_db)):
    attendance = db.query(Attendance).filter(Attendance.student_id == student_id).first()
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    attendance.status = status
    db.commit()
    db.refresh(attendance)
    return attendance

@router.delete("/attendance/")
def attendance_delete(student_id:int, db:Session=Depends(get_db)):
    Attendance_db=db.query(Attendance).filter(Attendance.student_id== student_id).first()
    if not Attendance_db:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    db.delete(Attendance_db)
    db.commit()
    return {"detail": "Attendance deleted successfully"}