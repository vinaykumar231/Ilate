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

router = APIRouter()


@router.post("/attendance/", response_model=AttendanceResponse)
def create_attendance(student_id: int, attendance: AttendanceCreate, db: Session = Depends(get_db)):
    user_db= db.query(LmsUsers).filter(LmsUsers.user_id== student_id).first()
    if not user_db:
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
    attendances = db.query(Attendance).filter(Attendance.student_id == student_id).all()
    return attendances

@router.put("/attendance/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(attendance_id: int, status: AttendanceStatus, db: Session = Depends(get_db)):
    attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    attendance.status = status
    db.commit()
    db.refresh(attendance)
    return attendance

@router.get("/attendance/date/{date}", response_model=List[AttendanceResponse])
def get_attendance_by_date(date: date, db: Session = Depends(get_db)):
    attendances = db.query(Attendance).filter(Attendance.date == date).all()
    return attendances

@router.get("/attendance/status/{status}", response_model=List[AttendanceResponse])
def get_attendance_by_status(status: AttendanceStatus, db: Session = Depends(get_db)):
    attendances = db.query(Attendance).filter(Attendance.status == status).all()
    return attendances