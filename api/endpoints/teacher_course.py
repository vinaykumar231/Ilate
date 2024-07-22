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
    # Check if the teacher exists
    teacher = db.query(Teacher).filter(Teacher.Teacher_id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    # Check if the courses exist
    courses = db.query(Course_content).filter(Course_content.id.in_(course_ids)).all()
    if not courses:
        raise HTTPException(status_code=404, detail="One or more courses not found")

     # Assign the courses to the teacher
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
    # Check if the user exists
    user = db.query(LmsUsers).filter(LmsUsers.user_id == current_user.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Query the database for assigned courses
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

    # Convert the ORM objects to Pydantic models
    return [CourseResponse.from_orm(course) for course in assigned_courses]

# @router.get("/teachers/{teacher_id}/courses", response_model=None)
# def get_teacher_courses(teacher_id: int, db: Session = Depends(get_db)):
#     try:
#         # Check if the teacher exists
#         teacher = db.query(Teacher).filter(Teacher.Teacher_id == teacher_id).first()
#         if not teacher:
#             raise HTTPException(status_code=404, detail="Teacher not found")

#         # Retrieve the courses assigned to the teacher
#         teacher_courses = db.query(TeacherCourse).filter(TeacherCourse.teacher_id == teacher_id).all()
#         if not teacher_courses:
#             raise HTTPException(status_code=404, detail="No courses assigned to this teacher")

#         course_ids = [tc.course_id for tc in teacher_courses]
#         courses = db.query(Course).filter(Course.id.in_(course_ids)).all()
#         course_names = [course.name for course in courses]

#         return {"teacher_name": teacher.name, "course_names": course_names}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to fetch teacher details: {str(e)}")

# @router.get("/teachers/{course_id}")
# def get_course(course_id: int, teacher_id: int, db: Session = Depends(get_db)):
#     try:
#         # Check if the course exists
#         course = db.query(Course).filter(Course.id == course_id).first()
#         if not course:
#             raise HTTPException(status_code=404, detail="Course not found")

#         # Check if the teacher is assigned to this course
#         teacher_course = db.query(TeacherCourse).filter(
#             TeacherCourse.teacher_id == teacher_id,
#             TeacherCourse.course_id == course_id
#         ).first()

#         if not teacher_course:
#             raise HTTPException(status_code=403, detail="Access forbidden: Teacher not assigned to this course")

#         # Get teacher details
#         teacher = db.query(Teacher).filter(Teacher.Teacher_id == teacher_id).first()

#         if not teacher:
#             raise HTTPException(status_code=404, detail="Teacher not found")

#         return {
#             "course_id": course.id,
#             "course_name": course.name,
#             "teacher_name": teacher.name
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to fetch teacher course details: {str(e)}")

# @router.put("/teachers/{teacher_id}/courses")
# def update_courses_for_teacher(teacher_id: int, course_ids: list[int], db: Session = Depends(get_db)):
#     # Check if the teacher exists
#     teacher = db.query(Teacher).filter(Teacher.Teacher_id == teacher_id).first()
#     if not teacher:
#         raise HTTPException(status_code=404, detail="Teacher not found")

#     # Check if the courses exist
#     courses = db.query(Course).filter(Course.id.in_(course_ids)).all()
#     if len(courses) != len(course_ids):
#         raise HTTPException(status_code=404, detail="One or more courses not found")

#     # Remove all current course assignments for the teacher
#     db.query(TeacherCourse).filter(TeacherCourse.teacher_id == teacher_id).delete()

#     # Assign the new courses to the teacher
#     for course in courses:
#         teacher_course = TeacherCourse(teacher_id=teacher.Teacher_id, course_id=course.id)
#         db.add(teacher_course)

#     try:
#         db.commit()
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail="Failed to update courses for teacher")

#     return {"message": "Courses updated successfully"}

# @router.delete("/teachers/{teacher_id}/courses")
# def remove_courses_from_teacher(teacher_id: int, course_ids: list[int], db: Session = Depends(get_db)):
#     # Check if the teacher exists
#     teacher = db.query(Teacher).filter(Teacher.Teacher_id == teacher_id).first()
#     if not teacher:
#         raise HTTPException(status_code=404, detail="Teacher not found")

#     # Check if the courses exist
#     courses = db.query(Course).filter(Course.id.in_(course_ids)).all()
#     if len(courses) != len(course_ids):
#         raise HTTPException(status_code=404, detail="One or more courses not found")

#     # Remove the courses from the teacher
#     for course in courses:
#         teacher_course = db.query(TeacherCourse).filter(
#             TeacherCourse.teacher_id == teacher_id,
#             TeacherCourse.course_id == course.id
#         ).first()
#         if teacher_course:
#             db.delete(teacher_course)

#     try:
#         db.commit()
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail="Failed to remove courses from teacher")

#     return {"message": "Courses removed successfully"}
