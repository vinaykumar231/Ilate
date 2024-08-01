from fastapi import FastAPI, Depends, HTTPException,APIRouter, Form
from datetime import datetime
from sqlalchemy.orm import Session
from db.session import get_db
from pydantic import BaseModel
from datetime import date
from typing import List
from auth.auth_bearer import JWTBearer, get_current_user,get_admin, get_teacher, get_admin_or_teacher, get_admin_or_student
from enum import Enum
from ..models.attendance import Attendance
from ..models.user import LmsUsers
from ..schemas import AttendanceStatus, AttendanceCreate, AttendanceResponse
import pytz
from ..models import Student
from ..models import Student,Course
from ..models import Course_content,CourseDetails
from ..models.teacher_course import TeacherCourse
import json
from pytz import timezone
from sqlalchemy import func

router = APIRouter()


class AttendanceBase(BaseModel):
    student_id: int
    course_content_id: int
    date: datetime
    status: List[str]

@router.post("/attendance/", response_model=List[AttendanceBase], dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
def create_attendance(
    student_ids: str = Form(...),
    course_content_id: int = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db)
):
    student_ids_list = student_ids.split(',')
    student_status_list = status.split(',')
    
    ist_now = datetime.now(timezone('Asia/Kolkata'))
    
    attendance_records = []
    
    for i, student_id in enumerate(student_ids_list):
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail=f"Student with id {student_id} not found")
        
        # Check if the attendance record already exists for the given student and course content on the same date
        existing_attendance = db.query(Attendance).filter(
            Attendance.student_id == student_id,
            Attendance.course_content_id == course_content_id,
            func.date(Attendance.date) == func.date(ist_now)  
        ).first()
        
        if existing_attendance:
            # Update existing record
            existing_attendance.status = [student_status_list[i]]
        else:
            # Create new record
            db_attendance = Attendance(
                student_id=student_id,
                course_content_id=course_content_id,
                status=[student_status_list[i]], 
                date=ist_now
            )
            db.add(db_attendance)
        
        db.commit()
        #db.refresh(existing_attendance)
        #for response
        attendance_records.append(AttendanceBase(
            student_id=student_id,
            course_content_id=course_content_id,
            date=ist_now,
            status=[student_status_list[i]]
        ))
    
    return attendance_records

@router.get("/attendance/", response_model=None)
def get_attendance(
    student_ids: str,
    db: Session = Depends(get_db)
):
    # Split the comma-separated student IDs into a list
    student_ids_list = student_ids.split(',')

    # Query attendance records for the given student_ids
    attendance_records = db.query(Attendance).filter(Attendance.student_id.in_(student_ids_list)).all()
    
    if not attendance_records:
        raise HTTPException(status_code=404, detail="No attendance records found for the provided student IDs")
    
    return attendance_records

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