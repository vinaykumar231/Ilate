from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from datetime import date
from sqlalchemy.orm import Session, joinedload
from db.session import get_db, SessionLocal
from ..models import Student, ContactInformation, PreEducation, Parent, LmsUsers, Inquiry, DemoFormFill, CourseDetails,Course, Standard, module,Subject, Module, Payment
from ..schemas import (StudentContactCreate, PreEducationCreate, ParentCreate,  StudentUpdate,
                       StudentContactUpdate, PreEducationUpdate, ParentInfoUpdate, CourseDetailsCreate, CourseDetailsUpdate)
from auth.auth_bearer import JWTBearer, get_current_user, get_admin, get_admin_or_student
#from ..models.Students import save_upload
from ..schemas import StudentCreate, StudentUpdate
from datetime import datetime
from typing import List, Union
from sqlalchemy import desc
from typing import Optional
import os
import uuid
import shutil
from datetime import date
import pytz
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import bcrypt
from pydantic import EmailStr, BaseModel


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

############################################################################################################################
def get_subject_by_id(db: Session, subject_id: int) -> dict:
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return {"id": subject.id, "name": subject.name}

def get_standard_by_id(db: Session, standard_id: int) -> dict:
    standard = db.query(Standard).filter(Standard.id == standard_id).first()
    if not standard:
        raise HTTPException(status_code=404, detail="Standard not found")
    return {"id": standard.id, "name": standard.name}

def get_module_by_id(db: Session, module_id: int) -> dict:
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return {"id": module.id, "name": module.name}

def get_course_by_id(db: Session, course_id: int) -> dict:
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"id": course.id, "name": course.name}

def get_payment_status_by_user_id(db: Session, user_id: int) -> bool:
    user = db.query(LmsUsers).filter(LmsUsers.user_id == user_id).first()
    if user:
        return user.is_payment_done
    return False

def check_payment_status(user_id: int, db: Session):
    payment_status = get_payment_status_by_user_id(db, user_id)
    if not payment_status:
        raise HTTPException(status_code=400, detail="Payment not made")
    
def get_payment_status_by_user_id(db_session: Session, user_id: int) -> bool:
    
    user = db_session.query(LmsUsers).filter(LmsUsers.user_id == user_id).first()
    if user:
        return user.is_payment_done
    else:
        return False 

def save_upload_file(upload_file: Optional[UploadFile]) -> Optional[str]:
    if not upload_file:
        return None
    
    try:
        unique_filename = str(uuid.uuid4()) + "_" + upload_file.filename
        file_path = os.path.join("static", "uploads", unique_filename)
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        
        # Convert backslashes to forward slashes
        file_path = file_path.replace("\\", "/")
        return file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")


######################################################################################################################
                # For sending Email
#######################################################################################################################

async def send_email(subject, email_to, body):
    # Set up the SMTP server
    smtp_server = 'smtp.gmail.com'  # Corrected SMTP server address for Gmail
    smtp_port = 587  # Corrected SMTP port for TLS encryption
    smtp_username = 'vinaykumar900417@gmail.com'  # Update with your email
    smtp_password = 'fgyc cjhy lfmb fddk'  # Update with your email password

    try:
        # Create a connection to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Start TLS encryption
        server.login(smtp_username, smtp_password)  # Login to the SMTP server

        # Construct the email message
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = email_to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        # Send the email
        server.sendmail(smtp_username, email_to, msg.as_string())

        # Close the connection to the SMTP server
        server.quit()

    except Exception as e:
        # Handle any exceptions, such as authentication failure
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
    
########################################################################################################

@router.post("/admission/", response_model=None)
async def fill_admission_form(
    first_name: str = Form(...),
    middle_name: str = Form(None),
    last_name: str = Form(...),
    date_of_birth: date = Form(...),
    gender: str = Form(...),
    nationality: str = Form(...),
    referral: str = Form(None),
    date_of_joining: date = Form(...),
    date_of_completion: date = Form(None),
    s_primary_no: str = Form(...),
    s_secondary_no: str = Form(None),
    s_primary_email: str = Form(...),
    s_secondary_email: str = Form(None),
    current_address: str = Form(...),
    permanent_address: str = Form(...),
    student_class: str = Form(...),
    school: str = Form(...),
    year_of_passing: int = Form(...),  
    percentage: float = Form(...),
    p_first_name: str = Form(...),
    p_middle_name: str = Form(None),
    p_last_name: str = Form(...),
    p_guardian: str = Form(...),
    p_primary_no: str = Form(...),
    # p_secondary_no: str = Form(None),
    p_primary_email: str = Form(...),
    # p_secondary_email: str = Form(None),
    subject: int = Form(...),
    standard: int = Form(...),
    module: int = Form(...),
    course: int = Form(...),
    id_proof: UploadFile = File(default=None),
    address_proof: UploadFile = File(default=None),
    db: Session = Depends(get_db),
    current_user: LmsUsers = Depends(get_current_user)
):
    existing_form = db.query(Student).filter(Student.user_id == current_user.user_id).first()
    if existing_form:
        raise HTTPException(status_code=400, detail="Admission form has already been submitted")
    
    # Handle file uploads
    id_proof_path = save_upload_file(id_proof)
    address_proof_path = save_upload_file(address_proof)
    #pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    try:
        parent_user_id = p_primary_email
        parent_password = p_first_name + "@123"
        hashed_password = bcrypt.hashpw((parent_password).encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        # Create student record
        db_student = Student(
            user_id=current_user.user_id,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender,
            referral=referral,
            nationality=nationality,
            date_of_joining=date_of_joining,
            date_of_completion=date_of_completion,
            id_proof=id_proof_path,
            Address_proof=address_proof_path
        )
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        

        # Create contact information record
        db_contact_info = ContactInformation(
            primary_no=s_primary_no,
            secondary_no=s_secondary_no,
            primary_email=s_primary_email,
            secondary_email=s_secondary_email,
            current_address=current_address,
            permanent_address=permanent_address,
            student_id=db_student.id
        )
        db.add(db_contact_info)

        # Create pre-education record
        db_pre_education = PreEducation(
            student_class=student_class,
            school=school,
            year_of_passing=year_of_passing,
            percentage=percentage,
            student_id=db_student.id
        )
        db.add(db_pre_education)

        # Create parent information record
        db_parent_info = Parent(
            p_first_name=p_first_name,
            p_middle_name=p_middle_name,
            p_last_name=p_last_name,
            guardian=p_guardian,
            primary_no=p_primary_no,
            p_user_id=parent_user_id,
            p_password=hashed_password,
            primary_email=p_primary_email,
            student_id=db_student.id
        )
        db.add(db_parent_info)
        db_parent_info.user_type = 'parent'
        db.commit()


        # Create course details record
        db_course_details = CourseDetails(
            subjects=subject,
            standards=standard,
            modules=module,
            courses=course,
            students=db_student.id
        )
        
        db.add(db_course_details)

        db.commit()
        current_user.user_type = 'student'
        current_user.is_formsubmited = True
        db.add(current_user)

        db.commit()

        # Generate unique URL for parent
        #unique_id = str(uuid.uuid4())
        #verification_url = f"http://192.168.29.82:8000/verify_parent/{unique_id}"

        # Send email to parent
        email_body = f"""
        <p>Dear {p_first_name},</p>
        <p>Your child, student ID :{db_student.id} {first_name} {last_name}, has been successfully admitted. Here are your login credentials:</p>
        <p>User ID: {parent_user_id}</p>
        <p>Password: {parent_password}</p>
        <p>Please use these credentials to log in for further updates.</p>
        <br>
        <p>Best regards,</p>
        <p>Vinay Kumar</p>
        <p>MaitriAI</p>
        <p>900417181</p>
        """
        await send_email(
            subject="Parent Account credentials",
            email_to=p_primary_email,
            body=email_body
        )
        return {"message": "Admission form has been submitted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to submit admission form: {str(e)}")

base_url_path = "http://192.168.29.82:8001"

@router.get("/admission/get_all", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
def get_all_admissions(db: Session = Depends(get_db)):
    students = get_all_students(db)
    if not students:
        raise HTTPException(status_code=404, detail="No students found")
    
    all_students_data = []
    for student in students:
        # Build the full URL for the ID proof and address proof
        id_proof_url = f"{base_url_path}/{student.id_proof}" if student.id_proof else None
        address_proof_url = f"{base_url_path}/{student.Address_proof}" if student.Address_proof else None

        def convert_to_names(ids: Union[int, List[int]], get_name_func):
            if isinstance(ids, int):
                return get_name_func(db, ids)
            elif isinstance(ids, list):
                return [get_name_func(db, id) for id in ids]
            return None

        student_data = {
            "user_id": student.user_id,
            "first_name": student.first_name,
            "middle_name": student.middle_name,
            "last_name": student.last_name,
            "date_of_birth": student.date_of_birth,
            "gender": student.gender,
            "nationality": student.nationality,
            "referral": student.referral,
            "date_of_joining": student.date_of_joining,
            "date_of_completion": student.date_of_completion,
            "id_proof_url": id_proof_url,
            "address_proof_url": address_proof_url,
            "contact_info": {
                "primary_no": student.contact_info.primary_no,
                "secondary_no": student.contact_info.secondary_no,
                "primary_email": student.contact_info.primary_email,
                "secondary_email": student.contact_info.secondary_email,
                "current_address": student.contact_info.current_address,
                "permanent_address": student.contact_info.permanent_address
            },
            "pre_education": {
                "student_class": student.pre_education.student_class,
                "school": student.pre_education.school,
                "year_of_passing": student.pre_education.year_of_passing,
                "percentage": student.pre_education.percentage
            },
            "parent_info": {
                "p_first_name": student.parent_info.p_first_name,
                "p_middle_name": student.parent_info.p_middle_name,
                "p_last_name": student.parent_info.p_last_name,
                "guardian": student.parent_info.guardian,
                "primary_no": student.parent_info.primary_no,
                "primary_email": student.parent_info.primary_email
            },
            "course_details": {
                "subjects": convert_to_names(student.course_details.subjects, get_subject_by_id),
                "standards": convert_to_names(student.course_details.standards, get_standard_by_id),
                "modules": convert_to_names(student.course_details.modules, get_module_by_id),
                "courses": convert_to_names(student.course_details.courses, get_course_by_id)
            }
        }
        all_students_data.append(student_data)

    return all_students_data

@router.get("/admission/{user_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_student)])
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    # Fetch student details
    student = get_student(db, user_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    # Check payment status
    is_payment_done = get_payment_status_by_user_id(db, user_id)

    # Build the full URL for the ID proof and address proof
    id_proof_url = f"{base_url_path}/{student.id_proof}" if student.id_proof else None
    address_proof_url = f"{base_url_path}/{student.Address_proof}" if student.Address_proof else None

    def convert_to_names(ids: Union[int, List[int]], get_name_func):
        if isinstance(ids, int):
            return get_name_func(db, ids)
        elif isinstance(ids, list):
            return [get_name_func(db, id) for id in ids]
        return None

    student_data = {
        "user_id": student.user_id,
        "student_id": student.id,
        "first_name": student.first_name,
        "middle_name": student.middle_name,
        "last_name": student.last_name,
        "date_of_birth": student.date_of_birth,
        "gender": student.gender,
        "nationality": student.nationality,
        "referral": student.referral,
        "date_of_joining": student.date_of_joining,
        "date_of_completion": student.date_of_completion,
        "id_proof_url": id_proof_url,
        "address_proof_url": address_proof_url,
        "contact_info": {
            "primary_no": student.contact_info.primary_no,
            "secondary_no": student.contact_info.secondary_no,
            "primary_email": student.contact_info.primary_email,
            "secondary_email": student.contact_info.secondary_email,
            "current_address": student.contact_info.current_address,
            "permanent_address": student.contact_info.permanent_address
        },
        "pre_education": {
            "student_class": student.pre_education.student_class,
            "school": student.pre_education.school,
            "year_of_passing": student.pre_education.year_of_passing,
            "percentage": student.pre_education.percentage
        },
        "parent_info": {
            "p_first_name": student.parent_info.p_first_name,
            "p_middle_name": student.parent_info.p_middle_name,
            "p_last_name": student.parent_info.p_last_name,
            "guardian": student.parent_info.guardian,
            "primary_no": student.parent_info.primary_no,
            "primary_email": student.parent_info.primary_email
        },
        "course_details": {
            "subjects": convert_to_names(student.course_details.subjects, get_subject_by_id),
            "standards": convert_to_names(student.course_details.standards, get_standard_by_id),
            "modules": convert_to_names(student.course_details.modules, get_module_by_id),
            "courses": convert_to_names(student.course_details.courses, get_course_by_id)
        },
         "payment_details": {
            "is_payment_done": is_payment_done
        }
    }

    # Fetch payment details if payment is done
    
    payment = db.query(Payment).filter(Payment.user_id == user_id).order_by(desc(Payment.created_on)).first()
    if payment:
            utc_now = pytz.utc.localize(datetime.utcnow())
            ist_now = utc_now.astimezone(pytz.timezone('Asia/Kolkata'))
            student_data["payment_details"].update({
                "payment_id": payment.payment_id,
                "amount": payment.amount,
                "payment_mode": payment.payment_mode,
                "payment_info": payment.payment_info,
                "other_info": payment.other_info,
                "created_on": ist_now
            })
    student_data["is_payment_done"] = is_payment_done
    return student_data



@router.put("/admission/{student_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_student)])
async def update_admission_form(
    student_id: int,
    first_name: str = Form(None),
    middle_name: str = Form(None),
    last_name: str = Form(None),
    date_of_birth: date = Form(None), 
    gender: str = Form(None),
    nationality: str = Form(None),
    referral: str = Form(None),
    date_of_joining: date = Form(None),  
    date_of_completion: date = Form(None),  
    primary_no: str = Form(None),
    secondary_no: str = Form(None),
    primary_email: str = Form(None),
    secondary_email: str = Form(None),
    current_address: str = Form(None),
    permanent_address: str = Form(None),
    student_class: str = Form(None),
    school: str = Form(None),
    year_of_passing: int = Form(None),
    percentage: float = Form(None),
    p_first_name: str = Form(None),
    p_middle_name: str = Form(None),
    p_last_name: str = Form(None),
    guardian: str = Form(None),
    subject: str = Form(None),
    standard: str = Form(None),
    module: str = Form(None),
    course: str = Form(None),
    id_proof: UploadFile = File(default=None),
    address_proof: UploadFile = File(default=None),
    db: Session = Depends(get_db),
    current_user: LmsUsers = Depends(get_current_user)
):
    # Check if the student exists
    existing_student = db.query(Student).filter(Student.id == student_id).first()
    if not existing_student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Convert date strings to datetime objects
    if date_of_birth:
        try:
            date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=422, detail="Invalid date format for date_of_birth")

    if date_of_joining:
        try:
            date_of_joining = datetime.strptime(date_of_joining, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=422, detail="Invalid date format for date_of_joining")

    if date_of_completion:
        try:
            date_of_completion = datetime.strptime(date_of_completion, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=422, detail="Invalid date format for date_of_completion")

    # Check if the student exists
    existing_student = db.query(Student).filter(Student.id == student_id).first()
    if not existing_student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Update student details
    if first_name is not None:
        existing_student.first_name = first_name
    if middle_name is not None:
        existing_student.middle_name = middle_name
    if last_name is not None:
        existing_student.last_name = last_name
    if date_of_birth is not None:
        existing_student.date_of_birth = date_of_birth
    if gender is not None:
        existing_student.gender = gender
    if nationality is not None:
        existing_student.nationality = nationality
    if referral is not None:
            existing_student.referral = referral
    if date_of_joining is not None:
        existing_student.date_of_joining = date_of_joining
    if date_of_completion is not None:
        existing_student.date_of_completion = date_of_completion
    if id_proof is not None:
        existing_student.id_proof = save_upload_file(id_proof)
    if address_proof is not None:
        existing_student.Address_proof = save_upload_file(address_proof)

    # Update contact information
    existing_contact_info = db.query(ContactInformation).filter(ContactInformation.student_id == student_id).first()
    if existing_contact_info:
        if primary_no is not None:
            existing_contact_info.primary_no = primary_no
        if secondary_no is not None:
            existing_contact_info.secondary_no = secondary_no
        if primary_email is not None:
            existing_contact_info.primary_email = primary_email
        if secondary_email is not None:
            existing_contact_info.secondary_email = secondary_email
        if current_address is not None:
            existing_contact_info.current_address = current_address
        if permanent_address is not None:
            existing_contact_info.permanent_address = permanent_address

    # Update pre-education details
    existing_pre_education = db.query(PreEducation).filter(PreEducation.student_id == student_id).first()
    if existing_pre_education:
        if student_class is not None:
            existing_pre_education.student_class = student_class
        if school is not None:
            existing_pre_education.school = school
        if year_of_passing is not None:
            existing_pre_education.year_of_passing = year_of_passing
        if percentage is not None:
            existing_pre_education.percentage = percentage

    # Update parent information
    existing_parent_info = db.query(Parent).filter(Parent.student_id == student_id).first()
    if existing_parent_info:
        if p_first_name is not None:
            existing_parent_info.p_first_name = p_first_name
        if p_middle_name is not None:
            existing_parent_info.p_middle_name = p_middle_name
        if p_last_name is not None:
            existing_parent_info.p_last_name = p_last_name
        if guardian is not None:
            existing_parent_info.guardian = guardian
        if primary_no is not None:
            existing_parent_info.primary_no = primary_no
        if secondary_no is not None:
            existing_parent_info.secondary_no = secondary_no
        if primary_email is not None:
            existing_parent_info.primary_email = primary_email
        if secondary_email is not None:
            existing_parent_info.secondary_email = secondary_email

    # Update course details
    existing_course_details = db.query(CourseDetails).filter(CourseDetails.students == student_id).first()
    if existing_course_details:
        if subject is not None:
            existing_course_details.subject = subject
        if standard is not None:
            existing_course_details.standard = standard
        if module is not None:
            existing_course_details.module = module
        if course is not None:
            existing_course_details.course = course

    db.commit()

    
    updated_data = {
        "student": {
            "first_name": existing_student.first_name,
            "middle_name": existing_student.middle_name,
            "last_name": existing_student.last_name,
            "date_of_birth": existing_student.date_of_birth,
            "gender": existing_student.gender,
            "nationality": existing_student.nationality,
            "referral": existing_student.referral,
            "date_of_joining": existing_student.date_of_joining,
            "date_of_completion": existing_student.date_of_completion,
            "id_proof": existing_student.id_proof,
            "address_proof": existing_student.Address_proof,
        },
        "contact_information": {
            "primary_no": existing_contact_info.primary_no if existing_contact_info else None,
            "secondary_no": existing_contact_info.secondary_no if existing_contact_info else None,
            "primary_email": existing_contact_info.primary_email if existing_contact_info else None,
            "secondary_email": existing_contact_info.secondary_email if existing_contact_info else None,
            "current_address": existing_contact_info.current_address if existing_contact_info else None,
            "permanent_address": existing_contact_info.permanent_address if existing_contact_info else None,
        },
        "pre_education": {
            "student_class": existing_pre_education.student_class if existing_pre_education else None,
            "school": existing_pre_education.school if existing_pre_education else None,
            "year_of_passing": existing_pre_education.year_of_passing if existing_pre_education else None,
            "percentage": existing_pre_education.percentage if existing_pre_education else None,
        },
        "parent_information": {
            "p_first_name": existing_parent_info.p_first_name if existing_parent_info else None,
            "p_middle_name": existing_parent_info.p_middle_name if existing_parent_info else None,
            "p_last_name": existing_parent_info.p_last_name if existing_parent_info else None,
            "guardian": existing_parent_info.guardian if existing_parent_info else None,
            "primary_no": existing_parent_info.primary_no if existing_parent_info else None,
            "secondary_no": existing_parent_info.secondary_no if existing_parent_info else None,
            "primary_email": existing_parent_info.primary_email if existing_parent_info else None,
            "secondary_email": existing_parent_info.secondary_email if existing_parent_info else None,
        },
        "course_details":{
            "subject":existing_course_details.subject if existing_course_details else None,
            "standard":existing_course_details.standard if existing_course_details else None,
            "module":existing_course_details.module if existing_course_details else None,
            "course":existing_course_details.course if existing_course_details else None,
            
        }
    }
    return updated_data


@router.delete("/admission/{user_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def delete_admission_form(user_id: int, db: Session = Depends(get_db)):
    existing_form = db.query(Student).filter(Student.user_id == user_id).first()
    if not existing_form:
        raise HTTPException(status_code=404, detail="Student not found")

    # Delete associated contact information, pre-education, parent, and student records
    db.query(ContactInformation).filter(ContactInformation.student_id == existing_form.id).delete()
    db.query(PreEducation).filter(PreEducation.student_id == existing_form.id).delete()
    db.query(Parent).filter(Parent.student_id == existing_form.id).delete()
    
    # Remove ID proof and address proof files
    if existing_form.id_proof and os.path.exists(existing_form.id_proof):
        os.remove(existing_form.id_proof)
    if existing_form. Address_proof and os.path.exists(existing_form. Address_proof):
        os.remove(existing_form. Address_proof)
    
    # Delete the student record
    db.delete(existing_form)
    db.commit()

    # Update the corresponding LmsUsers object
    lms_user = db.query(LmsUsers).filter(LmsUsers.user_id == user_id).first()
    if not lms_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Modify user_type and is_formsubmited attributes
    lms_user.user_type = 'student'
    lms_user.is_formsubmited = False
    lms_user.is_payment_done = False
    db.commit()

    return {"message": "Student data deleted successfully"}


@router.get("/dashboard_counts", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def get_dashboard_counts(db: Session = Depends(get_db)):
    total_users = db.query(LmsUsers).count()
    total_teachers = db.query(LmsUsers).filter(LmsUsers.user_type == "teacher").count()
    total_students = db.query(LmsUsers).filter(LmsUsers.user_type == "student").count()
    total_inquiries = db.query(Inquiry).count()
    total_demo = db.query(DemoFormFill).count()

    return {
        "user_count": total_users,
        "teacher_count": total_teachers,
        "student_count": total_students,
        "inquiry_count": total_inquiries,
        "demo_count": total_demo
    }


