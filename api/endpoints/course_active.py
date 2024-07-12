from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session, joinedload
from db.session import get_db
from ..models.payment import Payment
from ..models import Student, Course, LmsUsers, Batch,Module,Standard,Subject
from pydantic import BaseModel
from ..schemas import PaymentCreate,PaymentResponse
from auth.auth_bearer import JWTBearer, get_current_user,get_admin, get_teacher, get_admin_or_teacher, get_admin_or_student
from ..models import Student, ContactInformation, PreEducation, Parent, LmsUsers, Inquiry, DemoFormFill, CourseDetails,Course, Standard, module,Subject, Module, Payment
from typing import List
from sqlalchemy import desc
from datetime import datetime
from typing import Optional, Dict
import pytz
from sqlalchemy import desc, func
from api.models import CourseDetails, Content, LmsUsers, Course_content, Lesson
from typing import List
from pydantic import BaseModel
#from api.models import Course_content, CourseDetails, Student
from sqlalchemy import and_
import os
from dotenv import load_dotenv


load_dotenv()

router = APIRouter()



base_url_path = os.getenv("BASE_URL_PATH")  # Your base URL path

def get_user_contents(db: Session, user_id: int):
    contents_query = db.query(Content).join(
        CourseDetails,
        and_(
            Content.course_content_id == CourseDetails.course_content_id,
            CourseDetails.user_id == user_id,
            CourseDetails.is_active_course == True
        )
    ).options(joinedload(Content.lesson))

    contents = contents_query.all()

    if not contents:
        raise HTTPException(status_code=404, detail="No accessible content found for this user.")

    result = []
    for content in contents:
        lesson_data = {
            "lesson_id": content.lesson.lesson_id,
            "title": content.lesson.title,
            "description": content.lesson.description,
            "course_content_id": content.lesson.course_content_id,
            "content_info": {
                "id": content.id,
                "name": content.name,
                "description": content.description,
                "content_type": content.content_type,
                "content_path": [f"{base_url_path}/{path}" for path in content.content_path] if content.content_path else None
            }
        }
        result.append(lesson_data)

    return result


@router.get("/course_active/contents", response_model=List[dict])
def get_user_contents_endpoint(current_user: LmsUsers = Depends(get_current_user), db: Session = Depends(get_db)):
    contents = get_user_contents(db, current_user.user_id)
    return contents

############
@router.get("/course_content/", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
def get_course_content(
    course_id: int = None,
    subject_id: int = None,
    standard_id: int = None,
    module_id: int = None,
    is_active: bool = None,
    db: Session = Depends(get_db)
):
    query = db.query(Course_content)
    
    if course_id:
        query = query.filter(Course_content.course_id == course_id)
    if subject_id:
        query = query.filter(Course_content.subject_id == subject_id)
    if standard_id:
        query = query.filter(Course_content.standard_id == standard_id)
    if module_id:
        query = query.filter(Course_content.module_id == module_id)
    if is_active is not None:
        query = query.filter(Course_content.is_active == is_active)
    
    results = query.all()
    
    if not results:
        raise HTTPException(status_code=404, detail="No matching course content found")
    
    # Fetch names based on IDs
    for result in results:
        if result.course_id:
            course = db.query(Course).filter(Course.id == result.course_id).first()
            result.course_name = course.name if course else None
        
        if result.subject_id:
            subject = db.query(Subject).filter(Subject.id == result.subject_id).first()
            result.subject_name = subject.name if subject else None
        
        if result.standard_id:
            standard = db.query(Standard).filter(Standard.id == result.standard_id).first()
            result.standard_name = standard.name if standard else None
        
        if result.module_id:
            module = db.query(Module).filter(Module.id == result.module_id).first()
            result.module_name = module.name if module else None
    
    return results

@router.get("/course_contents/{content_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
def get_course_content_by_id(content_id: int, db: Session = Depends(get_db)):
    try:
        # Query for course content details
        course_content = db.query(Course_content).filter(Course_content.id == content_id).first()
        
        if not course_content:
            raise HTTPException(status_code=404, detail="Course content not found")

        # Query for related contents with their lessons
        contents_query = db.query(Content).filter(
            Content.course_content_id == content_id
        ).options(joinedload(Content.lesson))

        contents = contents_query.all()

        if not contents:
            raise HTTPException(status_code=404, detail="No content found for this course content.")

        result = {
            "id": course_content.id,
            "course_name": course_content.course.name,
            "subject_name": course_content.subject.name,
            "standard_name": course_content.standard.name,
            "module_name": course_content.module.name,
            "is_active": course_content.is_active,
            "lessons": []
        }

        for content in contents:
            lesson_data = {
                "lesson_id": content.lesson.lesson_id,
                "title": content.lesson.title,
                "description": content.lesson.description,
                "content_info": {
                    "id": content.id,
                    "name": content.name,
                    "description": content.description,
                    "content_type": content.content_type,
                    "content_path": [f"{base_url_path}/{path}" for path in content.content_path] if content.content_path else None
                }
            }
            
            # Check if the lesson is already in the result
            existing_lesson = next((l for l in result["lessons"] if l["lesson_id"] == lesson_data["lesson_id"]), None)
            if existing_lesson:
                existing_lesson["content_info"].append(lesson_data["content_info"])
            else:
                lesson_data["content_info"] = [lesson_data["content_info"]]
                result["lessons"].append(lesson_data)

        return result

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve course content: {str(e)}")

# @router.get("/course_active/{student_id}", response_model=None)
# def get_course_details(student_id: int, db: Session = Depends(get_db)):
#     # Retrieve the course details for the user
#     course_detail = db.query(CourseDetails).filter(CourseDetails.students == student_id).first()
    
#     if not course_detail.is_active_course:
#         raise HTTPException(status_code=404, detail="Course details not found for this user")

#     # Fetch related information
#     course = db.query(Course).filter(Course.id == course_detail.courses).first()
#     subject = db.query(Subject).filter(Subject.id == course_detail.subjects).first()
#     standard = db.query(Standard).filter(Standard.id == course_detail.standards).first()
#     module = db.query(Module).filter(Module.id == course_detail.modules).first()
#     student = db.query(Student).filter(Student.id == course_detail.students).first()

#     # Prepare the response
#     response_data = {
        
#     }

#     if course:
#         response_data["course_name"] = course.name
#     if subject:
#         response_data["subject_name"] = subject.name
#     if standard:
#         response_data["standard_name"] = standard.name
#     if module:
#         response_data["module_name"] = module.name
#     if student:
#         response_data["student_name"] = f"{student.first_name} {student.last_name}"

#     return response_data

# class CourseComparison(BaseModel):
#     course_id: int
#     subject_id: int
#     standard_id: int
#     module_id: int
#     is_match: bool
#     student_id: int
#     is_active: bool

# @router.get("/course_active/compare_course/{student_id}", response_model=List[CourseComparison])
# async def compare_course_details(student_id: int, db: Session = Depends(get_db)):
#     # Check if the student exists
#     student = db.query(Student).filter(Student.id == student_id).first()
#     if not student:
#         raise HTTPException(status_code=404, detail="Student not found")

#     # Get all CourseDetails for the student
#     student_courses = db.query(CourseDetails).filter(CourseDetails.students == student_id).all()
    
#     if not student_courses:
#         raise HTTPException(status_code=404, detail="No courses found for this student")

#     comparison_results = []
#     for student_course in student_courses:
#         # Find the corresponding Course_content
#         admin_course = db.query(Course_content).filter(
#             Course_content.course_id == student_course.courses,
#             Course_content.subject_id == student_course.subjects,
#             Course_content.standard_id == student_course.standards,
#             Course_content.module_id == student_course.modules
#         ).first()

#         is_match = admin_course is not None
#         comparison = CourseComparison(
#             course_id=student_course.courses,
#             subject_id=student_course.subjects,
#             standard_id=student_course.standards,
#             module_id=student_course.modules,
#             is_match=is_match,
#             student_id=student_id,
#             is_active=student_course.is_active_course and (admin_course.is_active if admin_course else False)
#         )
#         comparison_results.routerend(comparison)

#     return comparison_results