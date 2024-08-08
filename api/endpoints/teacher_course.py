from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from db.session import get_db
from fastapi import Header
from ..models.teacher_course import TeacherCourse
from ..models import Course_content
from ..models import (Employee, TeacherContact, Dependents, Education, EmergencyContact,LanguagesSpoken, Skill, LmsUsers, Teacher, Course)
from ..schemas import ( ContactInformationCreate, ContactInformationUpdate,EducationCreate, EducationUpdate, SkillCreate,SkillUpdate,
                        LanguagesSpokenCreate, LanguagesSpokenUpdate,EmergencyContactCreate, EmergencyContactUpdate,
                       DependentsCreate, DependentsUpdate, EmployeeCreate,EmployeeUpdate, TeacherCreate, TeacherUpdate)
from auth.auth_bearer import JWTBearer, get_current_user, get_admin, get_admin_or_teacher
from typing import List, Dict
from ..models.user import LmsUsers
from sqlalchemy import and_
from pydantic import BaseModel

router = APIRouter()

@router.post("/teachers/{teacher_id}/assign_courses")
def assign_courses_to_teacher(teacher_id: int, course_ids: list[int], db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.Teacher_id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    courses = db.query(Course_content).filter(Course_content.id.in_(course_ids)).all()
    if not courses:
        raise HTTPException(status_code=404, detail="One or more courses not found")

    for course in courses:
        teacher_course = TeacherCourse(
            teacher_id=teacher.Teacher_id,
            course_id=course.id,
            user_id=teacher.user_id,  
            is_assign_course=True
        )
        db.add(teacher_course)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to assign courses to teacher")

    return {"message": "Courses assigned successfully"}

class CourseResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True  # T
        
@router.get("/assigned_courses", response_model=List[CourseResponse])
def get_assigned_courses(
    current_user: LmsUsers = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(LmsUsers).filter(LmsUsers.user_id == current_user.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    assigned_courses = db.query(Course).join(
        TeacherCourse, 
        and_(
            TeacherCourse.course_id == Course.id,
            TeacherCourse.user_id == current_user.user_id,
            TeacherCourse.is_assign_course == True
        )
    ).all()

    if not assigned_courses:
        raise HTTPException(status_code=404, detail="No assigned courses found for this user")

    
    return [CourseResponse.from_orm(course) for course in assigned_courses]

