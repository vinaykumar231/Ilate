from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from db.session import get_db
from ..models import Student, ContactInformation, PreEducation, Parent, LmsUsers, Inquiry, DemoFormFill, CourseDetails
from ..schemas import (StudentContactCreate, PreEducationCreate, ParentCreate, StudentBase, StudentUpdate,
                       StudentContactUpdate, PreEducationUpdate, ParentInfoUpdate, CourseDetailsCreate, CourseDetailsUpdate)
from auth.auth_bearer import JWTBearer, get_current_user, get_admin, get_admin_or_student

router = APIRouter()


def get_student(db: Session, user_id: int):
    return db.query(Student) \
        .options(joinedload(Student.contact_info),
                 joinedload(Student.pre_education),
                 joinedload(Student.parent_info),
                 joinedload(Student.course_details)) \
        .filter(Student.user_id == user_id).first()


def get_all_students(db: Session):
    return db.query(Student) \
        .options(joinedload(Student.contact_info),
                 joinedload(Student.pre_education),
                 joinedload(Student.parent_info),
                 joinedload(Student.course_details)) \
        .all()


def get_contact_info(db: Session, student_id: int):
    return db.query(ContactInformation).filter(ContactInformation.student_id == student_id).first()


def get_pre_education(db: Session, student_id: int):
    return db.query(PreEducation).filter(PreEducation.student_id == student_id).first()


def get_parent_info(db: Session, student_id: int):
    return db.query(Parent).filter(Parent.student_id == student_id).first()

def get_course_details(db: Session, student_id: int):
    return db.query(CourseDetails).filter(CourseDetails.student_id == student_id).first()


def update_student(db: Session, student_id: int, student_data: StudentUpdate):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student:
        for key, value in student_data.dict(exclude_unset=True).items():
            setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
        return db_student
    else:
        raise HTTPException(status_code=404, detail="Student not found")


def update_contact_info(db: Session, student_id: int, contact_info: StudentContactUpdate):
    db_contact_info = db.query(ContactInformation).filter(ContactInformation.student_id == student_id).first()
    if db_contact_info:
        for key, value in contact_info.dict(exclude_unset=True).items():
            setattr(db_contact_info, key, value)
        db.commit()
        db.refresh(db_contact_info)
    else:
        raise HTTPException(status_code=404, detail="Contact information not found")


def update_pre_education(db: Session, student_id: int, pre_education: PreEducationUpdate):
    db_pre_education = db.query(PreEducation).filter(PreEducation.student_id == student_id).first()
    if db_pre_education:
        for key, value in pre_education.dict(exclude_unset=True).items():
            setattr(db_pre_education, key, value)
        db.commit()
        db.refresh(db_pre_education)
    else:
        raise HTTPException(status_code=404, detail="Pre-education information not found")


def update_parent_info(db: Session, student_id: int, parent_info: ParentInfoUpdate):
    db_parent_info = db.query(Parent).filter(Parent.student_id == student_id).first()
    if db_parent_info:
        for key, value in parent_info.dict(exclude_unset=True).items():
            setattr(db_parent_info, key, value)
        db.commit()
        db.refresh(db_parent_info)
    else:
        raise HTTPException(status_code=404, detail="Parent information not found")


def update_course_details(db: Session, student_id: int, course_details_update: CourseDetailsUpdate):
    db_course_details = get_course_details(db, student_id)
    if db_course_details:
        for key, value in course_details_update.dict().items():
            setattr(db_course_details, key, value)
        db.commit()
        db.refresh(db_course_details)
        return db_course_details
    else:
        raise HTTPException(status_code=404, detail="Course details not found")


def delete_student(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student:
        db.delete(student)
        db.commit()
        return True
    return False


# @router.post("/admission/", response_model=None)
# async def fill_admission_form(student_data: StudentBase, contact_info: StudentContactCreate,
#                               pre_education: PreEducationCreate, parent_info: ParentCreate,
#                               db: Session = Depends(get_db), current_user: LmsUsers = Depends(get_current_user)):
#     existing_form = db.query(Student).filter(Student.user_id == current_user.user_id).first()
#     if existing_form:
#         raise HTTPException(status_code=400, detail="Admission form has already been submitted")
#     # Create student record
#     db_student = Student(user_id=current_user.user_id, **student_data.dict())
#     db.add(db_student)
#     db.commit()
#     db.refresh(db_student)

#     # Create contact information record
#     db_contact_info = ContactInformation(**contact_info.dict(), student_id=db_student.id)
#     db.add(db_contact_info)
#     db.commit()

#     # Create pre-education record
#     db_pre_education = PreEducation(**pre_education.dict(), student_id=db_student.id)
#     db.add(db_pre_education)
#     db.commit()

#     # Create parent information record
#     db_parent_info = Parent(**parent_info.dict(), student_id=db_student.id)
#     db.add(db_parent_info)
#     db.commit()

#     db.refresh(db_student)
#     db.refresh(db_contact_info)
#     db.refresh(db_pre_education)
#     db.refresh(db_parent_info)

#     return {"message": "Admission form has been submitted successfully"}

@router.post("/admission/", response_model=None)
async def fill_admission_form(student_data: StudentBase, contact_info: StudentContactCreate,
                              pre_education: PreEducationCreate, parent_info: ParentCreate,
                              course_details: CourseDetailsCreate,
                              db: Session = Depends(get_db), current_user: LmsUsers = Depends(get_current_user)):

    existing_form = db.query(Student).filter(Student.user_id == current_user.user_id).first()
    if existing_form:
        raise HTTPException(status_code=400, detail="Admission form has already been submitted")

    # Create student record
    db_student = Student(user_id=current_user.user_id, **student_data.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    # Create contact information record
    db_contact_info = ContactInformation(**contact_info.dict(), student_id=db_student.id)
    db.add(db_contact_info)
    db.commit()

    # Create pre-education record
    db_pre_education = PreEducation(**pre_education.dict(), student_id=db_student.id)
    db.add(db_pre_education)
    db.commit()

    # Create parent information record
    db_parent_info = Parent(**parent_info.dict(), student_id=db_student.id)
    db.add(db_parent_info)
    db.commit()

    # Create course details record
    db_course_details = CourseDetails(**course_details.dict(), student_id=db_student.id)
    db.add(db_course_details)
    db.commit()

    db.refresh(db_student)
    db.refresh(db_contact_info)
    db.refresh(db_pre_education)
    db.refresh(db_parent_info)
    db.refresh(db_course_details)

    return {"message": "Admission form has been submitted successfully"}


@router.get("/admission/get_all", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
def get_all_student(db: Session = Depends(get_db)):
    student = get_all_students(db)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.get("/admission/{user_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_student)])
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    student = get_student(db,user_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/admission/{student_id}", response_model=None)
def update_student_admission(
        student_id: int,
        student_data: StudentUpdate = None,
        student_contact: StudentContactUpdate = None,
        student_parent: ParentInfoUpdate = None,
        student_education: PreEducationUpdate = None,
        course_details: CourseDetailsUpdate =None,
        current_user: LmsUsers = Depends(get_admin_or_student),
        db: Session = Depends(get_db)
):
    if current_user.user_type not in ["admin", "student"]:
        raise HTTPException(status_code=403, detail="You are not authorized to perform this action")
    # Check if the student exists
    # existing_student = get_student(db, user_id)
    # if existing_student is None:
    #     raise HTTPException(status_code=404, detail="Student not found")

    if student_data:
        update_student(db, student_id, student_data)

    if student_contact:
        existing_contact_info = get_contact_info(db, student_id)
        if existing_contact_info:
            update_contact_info(db, student_id, student_contact)
        else:
            raise HTTPException(status_code=404, detail="Contact information not found")

    if student_education:
        existing_pre_education = get_pre_education(db, student_id)
        if existing_pre_education:
            update_pre_education(db, student_id, student_education)
        else:
            raise HTTPException(status_code=404, detail="Pre-education information not found")

    if student_parent:
        existing_parent_info = get_parent_info(db, student_id)
        if existing_parent_info:
            update_parent_info(db, student_id, student_parent)
        else:
            raise HTTPException(status_code=404, detail="Parent information not found")
        
    if course_details:
        existing_course_details = get_course_details(db, student_id)
        if existing_course_details:
            update_course_details(db, student_id, course_details)
        else:
            raise HTTPException(status_code=404, detail="Course details not found")

    return {"message": "Data has been saved successfully"}


@router.delete("/admission/{student_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def delete_admission_form(student_id: int, db: Session = Depends(get_db)):
    existing_form = db.query(Student).filter(Student.id == student_id).first()
    if not existing_form:
        raise HTTPException(status_code=404, detail="Student not found")

    db.query(ContactInformation).filter(ContactInformation.student_id == existing_form.id).delete()
    db.query(PreEducation).filter(PreEducation.student_id == existing_form.id).delete()
    db.query(Parent).filter(Parent.student_id == existing_form.id).delete()
    db.delete(existing_form)
    db.commit()

    return {"message": "Student deleted successfully"}


@router.get("/dashboard_counts", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def get_dashboard_counts(db: Session = Depends(get_db)):
    total_users = db.query(LmsUsers).count()
    total_teachers = db.query(LmsUsers).filter(LmsUsers.user_type == "teacher").count()
    total_students = db.query(Student).count()
    total_inquiries = db.query(Inquiry).count()
    total_demo = db.query(DemoFormFill).count()

    return {
        "user_count": total_users,
        "teacher_count": total_teachers,
        "student_count": total_students,
        "inquiry_count": total_inquiries,
        "demo_count": total_demo
    }
