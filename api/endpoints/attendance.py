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
        
        existing_attendance = db.query(Attendance).filter(
            Attendance.student_id == student_id,
            Attendance.course_content_id == course_content_id,
            func.date(Attendance.date) == func.date(ist_now)  
        ).first()
        
        if existing_attendance:
            existing_attendance.status = [student_status_list[i]]
        else:
            db_attendance = Attendance(
                student_id=student_id,
                course_content_id=course_content_id,
                status=[student_status_list[i]], 
                date=ist_now
            )
            db.add(db_attendance)
        
        db.commit()
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
    student_ids_list = student_ids.split(',')
    all_records = db.query(Attendance).all()
    attendance_records = [record for record in all_records if record.student_id in student_ids_list]

    if not attendance_records:
        raise HTTPException(status_code=404, detail="No attendance records found for the provided student IDs")
    return attendance_records

@router.get("/attendance_students/", response_model=None)
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students

# @router.get("/attendance_students/", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
# def get_all_students(
#     course_id: int,
#     current_user: LmsUsers = Depends(get_current_user), 
#     db: Session = Depends(get_db)
# ):
#     students = []  # Initialize students as an empty list

#     if current_user.user_type == "teacher":
#         # Query the courses assigned to the teacher based on their user_id
#         assigned_courses = db.query(TeacherCourse).filter(
#             TeacherCourse.user_id == current_user.user_id,  # Use the teacher's user_id
#             TeacherCourse.is_assign_course == True
#         ).all()

#         # Debug print: Print teacher_id and course_id for each assigned course
#         for course in assigned_courses:
#             print(f"Teacher ID: {course.teacher_id}, Course ID: {course.course_id}")

#         if not assigned_courses:
#             raise HTTPException(status_code=404, detail="No courses assigned to this teacher")

#         # Extract the course_content_ids that the teacher is responsible for
#         course_content_ids = [course.course_id for course in assigned_courses]

#         # Match the students whose course details have these course_content_ids
#         students = db.query(Student).join(CourseDetails, Student.id == CourseDetails.students).filter(
#             CourseDetails.course_content_id == course_id,
#             CourseDetails.is_active_course == True  # Ensure the course is active
#         ).all()

#         if not students:
#             raise HTTPException(status_code=404, detail="No students found for the teacher's courses")

#     return students

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