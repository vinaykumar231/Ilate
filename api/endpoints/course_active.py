from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from ..models import Student, Course, LmsUsers, Batch,Module,Standard,Subject
from auth.auth_bearer import JWTBearer, get_admin_or_student
from api.models import CourseDetails

router = APIRouter()

@router.get("/course_active/{student_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_student)])
def get_course_details(student_id: int, db: Session = Depends(get_db)):
    # Retrieve the course details for the user
    course_detail = db.query(CourseDetails).filter(CourseDetails.students == student_id).first()
    
    if not course_detail.is_active_course:
        raise HTTPException(status_code=404, detail="Course details not found for this user")

    # Fetch related information
    course = db.query(Course).filter(Course.id == course_detail.courses).first()
    subject = db.query(Subject).filter(Subject.id == course_detail.subjects).first()
    standard = db.query(Standard).filter(Standard.id == course_detail.standards).first()
    module = db.query(Module).filter(Module.id == course_detail.modules).first()
    student = db.query(Student).filter(Student.id == course_detail.students).first()

    all_data =[]

    # Prepare the response
    response_data = {
        
    }

    if course:
        response_data["course_name"] = course.name
    if subject:
        response_data["subject_name"] = subject.name
    if standard:
        response_data["standard_name"] = standard.name
    if module:
        response_data["module_name"] = module.name
    if student:
        response_data["student_name"] = f"{student.first_name} {student.last_name}"

    all_data.append(response_data)

    return all_data