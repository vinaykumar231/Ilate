from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from db.session import get_db
from fastapi import Header
from ..models import (Employee, TeacherContact, Dependents, Education, EmergencyContact,LanguagesSpoken, Skill, LmsUsers, Teacher)
from ..schemas import ( ContactInformationCreate, ContactInformationUpdate,EducationCreate, EducationUpdate, SkillCreate,SkillUpdate,
                        LanguagesSpokenCreate, LanguagesSpokenUpdate,EmergencyContactCreate, EmergencyContactUpdate,
                       DependentsCreate, DependentsUpdate, EmployeeCreate,EmployeeUpdate, TeacherCreate, TeacherUpdate)
from auth.auth_bearer import JWTBearer, get_current_user, get_admin, get_admin_or_teacher
from typing import Optional

router = APIRouter()

def get_teacher(db: Session, user_id: int):
    query = db.query(Teacher).options(
        joinedload(Teacher.employee),
        joinedload(Teacher.contact_information),
        joinedload(Teacher.educations),
        joinedload(Teacher.dependents),
        joinedload(Teacher.emergency_contact),
        joinedload(Teacher.skills),
        joinedload(Teacher.languages_spoken)
    )
    if user_id:
        return query.filter(Teacher.user_id == user_id).first()
    return query.all()

def get_teacher1(db: Session, Teacher_id: int):
    query = db.query(Teacher).options(
        joinedload(Teacher.employee),
        joinedload(Teacher.contact_information),
        joinedload(Teacher.educations),
        joinedload(Teacher.dependents),
        joinedload(Teacher.emergency_contact),
        joinedload(Teacher.skills),
        joinedload(Teacher.languages_spoken)
    )
    if Teacher_id:
        return query.filter(Teacher.Teacher_id == Teacher_id).first()
    return query.all()

def get_all_teacher( db: Session):
    return db.query(Teacher) \
        .options(joinedload(Teacher.employee),
        joinedload(Teacher.contact_information),
        joinedload(Teacher.educations),
        joinedload(Teacher.dependents),
        joinedload(Teacher.emergency_contact),
        joinedload(Teacher.skills),
        joinedload(Teacher.languages_spoken )) \
        .all()


# def get_teacher(db: Session,user_id: int):
#     return db.query(Employee).filter(Teacher.user_id == user_id).first()

def get_employee(db: Session,Teacher_id: int):
    return db.query(Employee).filter(Employee.Teacher_id == Teacher_id).first()

def get_teacher_contact_info(db: Session,Teacher_id: int):
    return db.query(TeacherContact).filter(TeacherContact.Teacher_id == Teacher_id).first()


def get_teacher_education(db: Session, Teacher_id: int):
    return db.query(Education).filter(Education.Teacher_id ==Teacher_id).first()


def get_teacher_depends(db: Session, Teacher_id: int):
    return db.query(Dependents).filter(Dependents.Teacher_id ==Teacher_id).first()

def get_teacher_emergency_contact(db: Session, Teacher_id: int):
    return db.query(EmergencyContact).filter(EmergencyContact.Teacher_id == Teacher_id).first()

def get_teacher_language_spoken(db: Session, Teacher_id: int):
    return db.query(LanguagesSpoken).filter(LanguagesSpoken.Teacher_id == Teacher_id).first()

def get_teacher_skills(db: Session, Teacher_id: int):
    return db.query(Skill).filter(Skill.Teacher_id == Teacher_id).first()



def update_teacher_data(db: Session, Teacher_id: int, teacher_data: TeacherUpdate):
    db_teacher_data = db.query(Teacher).filter(Teacher.Teacher_id ==Teacher_id).first()
    if db_teacher_data:
        for key, value in teacher_data.dict(exclude_unset=True).items():
            setattr(db_teacher_data, key, value)
        db.commit()
        db.refresh(db_teacher_data)
        return db_teacher_data
    else:
        raise HTTPException(status_code=404, detail="Teacher  not found")

def update_employee(db: Session, Teacher_id: int, employee_data: EmployeeUpdate):
    db_employee = db.query(Employee).filter(Employee.Teacher_id ==Teacher_id).first()
    if db_employee:
        for key, value in employee_data.dict(exclude_unset=True).items():
            setattr(db_employee, key, value)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    else:
        raise HTTPException(status_code=404, detail="Teacher  not found")


def update_teacher_contact_info(db: Session, Teacher_id: int, teacher_contact_info: ContactInformationUpdate):
    db_teacher_contact_info = db.query(TeacherContact).filter(TeacherContact.Teacher_id == Teacher_id).first()
    if  db_teacher_contact_info:
        for key, value in teacher_contact_info.dict(exclude_unset=True).items():
            setattr(db_teacher_contact_info, key, value)
        db.commit()
        db.refresh(db_teacher_contact_info)
    else:
        raise HTTPException(status_code=404, detail="Contact information not found")


def update_teacher_education(db: Session, Teacher_id: int, teacher_education: EducationUpdate):
    db_teacher_education = db.query(Education).filter(Education.Teacher_id == Teacher_id).first()
    if db_teacher_education:
        for key, value in teacher_education.dict(exclude_unset=True).items():
            setattr(db_teacher_education, key, value)
        db.commit()
        db.refresh(db_teacher_education)
    else:
        raise HTTPException(status_code=404, detail="education information not found")


def update_teacher_depends(db: Session, Teacher_id: int, teacher_depends: DependentsUpdate):
    db_teacher_depends = db.query(Dependents).filter(Dependents.Teacher_id == Teacher_id).first()
    if  db_teacher_depends:
        for key, value in teacher_depends.dict(exclude_unset=True).items():
            setattr( db_teacher_depends, key, value)
        db.commit()
        db.refresh( db_teacher_depends)
    else:
        raise HTTPException(status_code=404, detail="teacher_depends information not found")
    
def update_teacher_emergencyContact(db: Session, Teacher_id: int, teacher_emergencyContact: EmergencyContactUpdate):
    db_teacher_emergencyContact = db.query(EmergencyContact).filter(EmergencyContact.Teacher_id == Teacher_id).first()
    if  db_teacher_emergencyContact:
        for key, value in teacher_emergencyContact.dict(exclude_unset=True).items():
            setattr( db_teacher_emergencyContact, key, value)
        db.commit()
        db.refresh( db_teacher_emergencyContact)
    else:
        raise HTTPException(status_code=404, detail="teacher_emergencyContact information not found")
    
def update_teacher_LanguagesSpoken(db: Session, Teacher_id: int, teacher_LanguagesSpoken:  LanguagesSpokenUpdate):
    db_teacher_LanguagesSpoken = db.query(LanguagesSpoken).filter(LanguagesSpoken.Teacher_id == Teacher_id).first()
    if  db_teacher_LanguagesSpoken:
        for key, value in teacher_LanguagesSpoken.dict(exclude_unset=True).items():
            setattr( db_teacher_LanguagesSpoken, key, value)
        db.commit()
        db.refresh( db_teacher_LanguagesSpoken)
    else:
        raise HTTPException(status_code=404, detail="teacher_LanguagesSpoken information not found")
    
def update_skill(db: Session, Teacher_id: int, skill_update: SkillUpdate):
    db_skill = db.query(Skill).filter(Skill.Teacher_id == Teacher_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    for key, value in skill_update.dict().items():
        setattr(db_skill, key, value)
    db.commit()
    db.refresh(db_skill)
    return db_skill


@router.post("/teachers/", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
async def fill_teacher_data(
    teacher_data : TeacherCreate,
    employee: EmployeeCreate,
    teacher_contact_info: ContactInformationCreate,
    dependent: DependentsCreate,
    education: EducationCreate,
    skill: SkillCreate,
    emergency_contact: EmergencyContactCreate,
    languages_spoken: LanguagesSpokenCreate,
    db: Session = Depends(get_db),
    current_user: LmsUsers = Depends(get_current_user)
):
    try:
        existing_form = db.query(Teacher).filter(Teacher.user_id == current_user.user_id).first()
        if existing_form:
            raise HTTPException(status_code=400, detail="Teacher data has already been submitted")

        db_teacher = Teacher(**teacher_data.dict(),user_id=current_user.user_id)
        db.add(db_teacher)
        db.commit()
        db.refresh(db_teacher)

        db_employee = Employee(**employee.dict(), Teacher_id=db_teacher.Teacher_id)
        db.add(db_employee)
        db.commit()

        db_teacher_contact = TeacherContact(**teacher_contact_info.dict(), Teacher_id=db_teacher.Teacher_id)
        db.add(db_teacher_contact)
        db.commit()

        db_dependents = Dependents(**dependent.dict(), Teacher_id=db_teacher.Teacher_id)
        db.add(db_dependents)
        db.commit()

        db_education = Education(**education.dict(), Teacher_id=db_teacher.Teacher_id)
        db.add(db_education)
        db.commit()

        db_skill = Skill(**skill.dict(), Teacher_id=db_teacher.Teacher_id)
        db.add(db_skill)
        db.commit()

        db_emergency_contact = EmergencyContact(**emergency_contact.dict(), Teacher_id=db_teacher.Teacher_id)
        db.add(db_emergency_contact)
        db.commit()

        db_languages_spoken = LanguagesSpoken(**languages_spoken.dict(), Teacher_id=db_teacher.Teacher_id)
        db.add(db_languages_spoken)
        db.commit()

        current_user.user_type = 'teacher'
        current_user.is_formsubmited = True
        db.add(current_user)
        db.commit()

        return {"message": "Teacher all data has been submitted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create teacher details: {str(e)}")


@router.get("/teachers/get_all", response_model=None, dependencies=[Depends(JWTBearer(get_admin))])
def get_all_teachers(db: Session = Depends(get_db)):
    try:
        teachers = get_all_teacher(db)
        if not teachers:
            raise HTTPException(status_code=404, detail="Teachers not found")
        return teachers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch teacher details: {str(e)}")

@router.get("/teachers/{user_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
def get_Teacher_user_profile(user_id: int, db: Session = Depends(get_db)):
    try:
        teacher = get_teacher(db, user_id)
        
        if teacher is None:
            raise HTTPException(status_code=404, detail="Teacher not found")

        # Get the first related object or None if the relationship is empty
        contact_info = teacher.contact_information[0] if teacher.contact_information else None
        dependent = teacher.dependents[0] if teacher.dependents else None
        education = teacher.educations[0] if teacher.educations else None
        emergency_contact = teacher.emergency_contact[0] if teacher.emergency_contact else None
        language_spoken = teacher.languages_spoken[0] if teacher.languages_spoken else None
        skill = teacher.skills[0] if teacher.skills else None
        
        teacher_data = {
            "Teacher_id": teacher.Teacher_id,
            "user_id": teacher.user_id,
            "name": teacher.name,
            "email": teacher.email,
            "contact_info": {
                "primary_number": contact_info.primary_number if contact_info else None,
                "secondary_number": contact_info.secondary_number if contact_info else None,
                "primary_email_id": contact_info.primary_email_id if contact_info else None,
                "secondary_email_id": contact_info.secondary_email_id if contact_info else None,
                "current_address": contact_info.current_address if contact_info else None,
                "permanent_address": contact_info.permanent_address if contact_info else None
            },
            "dependent": {
                "id": dependent.id if dependent else None,
                "dependent_name": dependent.dependent_name if dependent else None,
                "relation": dependent.realtion if dependent else None,
                "date_of_birth": dependent.date_of_birth if dependent else None
            },
            "education": {
                "id": education.id if education else None,
                "education_level": education.education_level if education else None,
                "institution": education.institution if education else None,
                "specialization": education.specialization if education else None,
                "field_of_study": education.field_of_study if education else None,
                "year_of_passing": education.year_of_passing if education else None,
                "percentage": education.percentage if education else None
            },
            "emergency_contact": {
                "id": emergency_contact.id if emergency_contact else None,
                "emergency_contact_name": emergency_contact.emergency_contact_name if emergency_contact else None,
                "relation": emergency_contact.relation if emergency_contact else None,
                "emergency_contact_number": emergency_contact.emergency_contact_number if emergency_contact else None
            },
            "languages_spoken": {
                "id": language_spoken.id if language_spoken else None,
                "languages": language_spoken.languages if language_spoken else None
            },
            "skill": {
                "id": skill.id if skill else None,
                "skill": skill.skill if skill else None,
                "certification": skill.certification if skill else None,
                "license": skill.license if skill else None
            }
        }
        
        return teacher_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch teacher details: {str(e)}")

# @router.get("/teachers/{user_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
# def get_Teacher_user_profile( user_id: int, db: Session = Depends(get_db)):
#     teacher = get_teacher(db, user_id)
#     if teacher is None:
#         raise HTTPException(status_code=404, detail="Teacher not found")
#     return teacher

def increment_content_file_count(db: Session, teacher_id: int):
    teacher = db.query(Teacher).filter(Teacher.Teacher_id == teacher_id).first()
    if teacher:
        teacher.content_file_count += 1
        db.commit()

def decrement_content_file_count(db: Session, teacher_id: int):
    teacher = db.query(Teacher).filter(Teacher.Teacher_id == teacher_id).first()
    if teacher:
        if teacher.content_file_count > 0:
            teacher.content_file_count -= 1
            db.commit()

@router.put("/teachers/update/{Teacher_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
async def update_teacher_profile(
        Teacher_id: int,
        teacher_data: Optional[TeacherUpdate] = None,
        employee_data: Optional[EmployeeUpdate] = None,
        teacher_contact_info: Optional[ContactInformationUpdate] = None,
        dependent: Optional[DependentsUpdate] = None,
        education: Optional[EducationUpdate] = None,
        skill: Optional[SkillUpdate] = None,
        emergency_contact: Optional[EmergencyContactUpdate] = None,
        languages_spoken: Optional[LanguagesSpokenUpdate] = None,
        db: Session = Depends(get_db),
        current_user: LmsUsers = Depends(get_current_user)
):
    try:
        # Check if the teacher exists
        existing_teacher = get_teacher1(db, Teacher_id)
        if not existing_teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

        # Helper function to handle conditional updates
        def handle_update(model_instance, update_data):
            for field, value in update_data.items():
                if value is not None:
                    setattr(model_instance, field, value)

        # Update teacher data if provided
        if teacher_data:
            handle_update(existing_teacher, teacher_data.dict(exclude_unset=True))

        # Fetch and update related data
        existing_employee = get_employee(db, Teacher_id)
        if employee_data and existing_employee:
            handle_update(existing_employee, employee_data.dict(exclude_unset=True))

        existing_contact_info = get_teacher_contact_info(db, Teacher_id)
        if teacher_contact_info and existing_contact_info:
            handle_update(existing_contact_info, teacher_contact_info.dict(exclude_unset=True))

        existing_dependent = get_teacher_depends(db, Teacher_id)
        if dependent and existing_dependent:
            handle_update(existing_dependent, dependent.dict(exclude_unset=True))

        existing_education = get_teacher_education(db, Teacher_id)
        if education and existing_education:
            handle_update(existing_education, education.dict(exclude_unset=True))

        existing_skill = get_teacher_skills(db, Teacher_id)
        if skill and existing_skill:
            handle_update(existing_skill, skill.dict(exclude_unset=True))

        existing_emergency_contact = get_teacher_emergency_contact(db, Teacher_id)
        if emergency_contact and existing_emergency_contact:
            handle_update(existing_emergency_contact, emergency_contact.dict(exclude_unset=True))

        existing_languages_spoken = get_teacher_language_spoken(db, Teacher_id)
        if languages_spoken and existing_languages_spoken:
            handle_update(existing_languages_spoken, languages_spoken.dict(exclude_unset=True))

        # Commit the updates to the database
        db.commit()

        # Fetch the updated data
        updated_teacher = get_teacher1(db, Teacher_id)
        updated_employee = get_employee(db, Teacher_id)
        updated_contact_info = get_teacher_contact_info(db, Teacher_id)
        updated_dependent = get_teacher_depends(db, Teacher_id)
        updated_education = get_teacher_education(db, Teacher_id)
        updated_skill = get_teacher_skills(db, Teacher_id)
        updated_emergency_contact = get_teacher_emergency_contact(db, Teacher_id)
        updated_languages_spoken = get_teacher_language_spoken(db, Teacher_id)


        return {
            "Teacher_data": updated_teacher,
            "employee_data": updated_employee,
            "contact_info": updated_contact_info,
            "dependent": updated_dependent,
            "education": updated_education,
            "skill": updated_skill,
            "emergency_contact": updated_emergency_contact,
            "languages_spoken": updated_languages_spoken
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update teacher details: {str(e)}")



@router.delete("/teachers/{user_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
async def delete_teacher(user_id: int, db: Session = Depends(get_db)):
    try:
        # Check if the teacher exists
        existing_teacher = db.query(Teacher).filter(Teacher.user_id == user_id).first()
        if not existing_teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

        # Delete associated data from other tables
        db.query(Employee).filter(Employee.Teacher_id == existing_teacher.Teacher_id).delete()
        db.query(TeacherContact).filter(TeacherContact.Teacher_id == existing_teacher.Teacher_id).delete()
        db.query(Education).filter(Education.Teacher_id == existing_teacher.Teacher_id).delete()
        db.query(Dependents).filter(Dependents.Teacher_id == existing_teacher.Teacher_id).delete()
        db.query(EmergencyContact).filter(EmergencyContact.Teacher_id == existing_teacher.Teacher_id).delete()
        db.query(LanguagesSpoken).filter(LanguagesSpoken.Teacher_id == existing_teacher.Teacher_id).delete()
        db.query(Skill).filter(Skill.Teacher_id == existing_teacher.Teacher_id).delete()

        # Delete the teacher
        db.delete(existing_teacher)
        db.commit()
        lms_user = db.query(LmsUsers).filter(LmsUsers.user_id == user_id).first()
        if not lms_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Modify user_type and is_formsubmited attributes
        lms_user.user_type = 'teacher'
        lms_user.is_formsubmited = False
        db.commit()

        return {"message": "Teacher and associated data deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete teacher details: {str(e)}")



@router.get("/teacher/dashboard_counts", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def get_teacher_dashboard_counts(db: Session = Depends(get_db)):
    try:
        total_teachers_from_users = db.query(LmsUsers).filter(LmsUsers.user_type == "teacher").count()
        total_employees = db.query(Teacher).count()
        total_teacher_contacts = db.query(TeacherContact).count()
        total_dependents = db.query(Dependents).count()
        total_educations = db.query(Education).count()
        total_languages_spoken = db.query(LanguagesSpoken).count()
        total_skills = db.query(Skill).count()
        total_emergency_contacts = db.query(EmergencyContact).count()

        return {
            "total_teachers_from_users": total_teachers_from_users,
            "employee_count": total_employees,
            "teacher_contact_count": total_teacher_contacts,
            "dependents_count": total_dependents,
            "education_count": total_educations,
            "languages_spoken_count": total_languages_spoken,
            "skills_count": total_skills,
            "emergency_contact_count": total_emergency_contacts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create teacher dashboard: {str(e)}")