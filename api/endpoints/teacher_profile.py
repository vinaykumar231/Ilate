from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from db.session import get_db
from fastapi import Header
from ..models import (Employee, TeacherContact, Dependents, Education, EmergencyContact,LanguagesSpoken, Skill, LmsUsers, Teacher)
from ..schemas import ( ContactInformationCreate, ContactInformationUpdate,EducationCreate, EducationUpdate, SkillCreate,SkillUpdate,
                        LanguagesSpokenCreate, LanguagesSpokenUpdate,EmergencyContactCreate, EmergencyContactUpdate,
                       DependentsCreate, DependentsUpdate, EmployeeCreate,EmployeeUpdate, TeacherCreate, TeacherUpdate)
from auth.auth_bearer import JWTBearer, get_current_user, get_admin, get_admin_or_teacher

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


@router.post("/teachers/", response_model=None)
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

    return {"message": "Teacher all data has been submitted successfully"}

from fastapi import Depends, HTTPException

@router.get("/teachers/get_all", response_model=None, dependencies=[Depends(JWTBearer(get_admin))])
def get_all_teachers(db: Session = Depends(get_db)):
    teachers = get_all_teacher(db)
    if not teachers:
        raise HTTPException(status_code=404, detail="Teachers not found")
    return teachers


@router.get("/teachers/{ user_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
def get_Teacher_user_profile( user_id: int, db: Session = Depends(get_db)):
    teacher = get_teacher(db, user_id)
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

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

@router.put("/teachers/update/{Teacher_id}", response_model=None)
async def update_teacher_profile(
        Teacher_id: int,
        teacher_data: TeacherUpdate = None,
        employee_data: EmployeeUpdate = None,
        teacher_contact_info: ContactInformationUpdate = None,
        dependent: DependentsUpdate = None,
        education: EducationUpdate = None,
        skill: SkillUpdate = None,
        emergency_contact: EmergencyContactUpdate = None,
        languages_spoken: LanguagesSpokenUpdate = None,
        db: Session = Depends(get_db),
        current_user: LmsUsers = Depends(get_current_user)
):
    existing_teacher = get_teacher(db, Teacher_id)
    if not existing_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    if teacher_data:
        update_teacher_data(db, Teacher_id, teacher_data)
    
    if employee_data:
        update_employee(db, Teacher_id, employee_data)
    
    if teacher_contact_info:
        update_teacher_contact_info(db, Teacher_id, teacher_contact_info)

    if dependent:
        update_teacher_depends(db, Teacher_id, dependent)
    
    if education:
        update_teacher_education(db, Teacher_id, education)

    if skill:
        update_skill(db, Teacher_id, skill)
    
    if emergency_contact:
        update_teacher_emergencyContact(db, Teacher_id, emergency_contact)
    
    if languages_spoken:
        update_teacher_LanguagesSpoken(db, Teacher_id, languages_spoken)

    # Increment content file count if new file is uploaded
    if teacher_data and teacher_data.content_file:
        increment_content_file_count(db, Teacher_id)

    # Decrement content file count if file is removed
    if teacher_data and teacher_data.remove_content_file:
        decrement_content_file_count(db, Teacher_id)

    return {"message": "Teacher data has been updated successfully"}


@router.delete("/teachers/{Teacher_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
async def delete_teacher(Teacher_id: int, db: Session = Depends(get_db)):
    # Check if the teacher exists
    existing_teacher = db.query(Teacher).filter(Teacher.Teacher_id == Teacher_id).first()
    if not existing_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    # Delete associated data from other tables
    db.query(Employee).filter(Employee.Teacher_id == Teacher_id).delete()
    db.query(TeacherContact).filter(TeacherContact.Teacher_id == Teacher_id).delete()
    db.query(Education).filter(Education.Teacher_id == Teacher_id).delete()
    db.query(Dependents).filter(Dependents.Teacher_id == Teacher_id).delete()
    db.query(EmergencyContact).filter(EmergencyContact.Teacher_id == Teacher_id).delete()
    db.query(LanguagesSpoken).filter(LanguagesSpoken.Teacher_id == Teacher_id).delete()
    db.query(Skill).filter(Skill.Teacher_id == Teacher_id).delete()

    # Delete the teacher
    db.delete(existing_teacher)
    db.commit()

    return {"message": "Teacher and associated data deleted successfully"}


@router.get("/teacher/dashboard_counts", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def get_teacher_dashboard_counts(db: Session = Depends(get_db)):
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