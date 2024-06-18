from fastapi import APIRouter, Depends, HTTPException
from ..models import Parent
from ..schemas import ParentCreate
from sqlalchemy.orm import Session
from db.session import get_db, SessionLocal
from ..models import Student, ContactInformation, PreEducation, Parent, LmsUsers, Inquiry, DemoFormFill, CourseDetails,Course, Standard, module,Subject, Module, Payment
from auth.auth_bearer import JWTBearer, get_admin_or_parent,get_user_id_from_token, get_admin_student_teacher_parent

######
from sqlalchemy import desc
from fastapi import Request, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.auth_handler import decodeJWT
from db.session import get_db
from sqlalchemy.orm import Session
from typing import Optional
from api.models.user import LmsUsers
from jwt import PyJWTError
import time
from typing import Any
import jwt
from decouple import config
from jwt import PyJWTError
from pydantic import EmailStr, BaseModel
import bcrypt
from .std_profile import send_email
####
from ..models.announcement import Announcement


router = APIRouter()


#########################################################################################################################
                    # for parent Login  or generate token
##########################################################################################################################

# JWT_SECRET = config('secret')
# JWT_ALGORITHM = config('algorithm')

# def signJWT(parent_id: str, user_type: str) -> tuple[str, float]:
#     expiration_time = time.time() + 1 * 24 * 60 * 60
#     payload = {
#         "parent_id": parent_id,
#         "user_type": user_type,
#         "exp": expiration_time
#     }
#     token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
#     return token, expiration_time

# def decodeJWT(token: str) -> dict | None:
#     try:
#         decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
#         if decoded_token.get("exp") and decoded_token["exp"] < time.time():
#             return None
#         if "parent_id" not in decoded_token or "user_type" not in decoded_token:
#             return None
#         return decoded_token
#     except PyJWTError:
#         return None

# class JWTBearer(HTTPBearer):
#     def __init__(self, auto_error: bool = True):
#         super(JWTBearer, self).__init__(auto_error=auto_error)

#     async def __call__(self, request: Request):
#         credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
#         if credentials:
#             if not credentials.scheme == "Bearer":
#                 raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
#             if not self.verify_jwt(credentials.credentials):
#                 raise HTTPException(status_code=403, detail="Invalid token or expired token.")
#             return credentials.credentials
#         else:
#             raise HTTPException(status_code=403, detail="Invalid authorization code.")

#     @staticmethod
#     def verify_jwt(jwt_token: str) -> bool:
#         try:
#             payload = decodeJWT(jwt_token)
#             return payload is not None
#         except Exception as e:
#             print(str(e))
#             return False
        
# def get_parent_id_from_token(token: str = Depends(JWTBearer())):
#     payload = decodeJWT(token)
    
#     if payload:
#         return payload.get("parent_id")
        
#     else:
#         raise HTTPException(status_code=403, detail="Invalid or expired token")
    
# def get_admin_or_parent(parent_id: int = Depends(get_parent_id_from_token), db: Session = Depends(get_db)) -> Optional[Parent]:
#     user = db.query(Parent).filter(Parent.parent_id == parent_id).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="parent not found")
#     if user.user_type not in ["parent", "admin"]:
#         raise HTTPException(status_code=403, detail="You are not authorized to perform this action")
#     return user

##################################################################################################################################
                     

# class ParentLoginInput(BaseModel):
#     primary_email: EmailStr
#     p_password: str

# @staticmethod
# def parent_login(credential: ParentLoginInput):
#     try:
#         session = SessionLocal()
#         user = session.query(Parent).filter(Parent.primary_email == credential.primary_email).first()
        
#         if not user:
#             raise HTTPException(404, detail=f"Record with Email: {credential.primary_email} not found")

#         if user.p_password is None:
#             raise HTTPException(403, detail='Password not set for this user')


#         if bcrypt.checkpw(credential.p_password.encode('utf-8'), user.p_password.encode('utf-8')):
#             token, exp = signJWT(user.parent_id, user.user_type)
#             if user.user_type == "parent":
#                 response = {
#                     'token': token,
#                     'exp': exp,
#                     'parent_id': user.parent_id,
#                     'p_first_name': user.p_first_name,
#                     'primary_email': user.primary_email,
#                     'user_type': user.user_type,
#                 }
#                 return response
#             else:
#                 raise HTTPException(403, detail='Unauthorized access')
#         else:
#             raise HTTPException(403, detail='Invalid email or password')

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
#############################################################################################################################

# @router.post('/parent_login')
# async def parent_login_route(credential: ParentLoginInput):
#     try:
#         response = parent_login(credential)
#         return response
#     except HTTPException as e:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
# @staticmethod
# def validate_password(password):
#         return len(password) >= 8

# @router.put("/parent/change_password")
# async def parent_change_password(current_password: str, new_password: str, confirm_new_password: str, parent_id: int= Depends(get_parent_id_from_token), db: Session = Depends(get_db)):
#     try:
#         parent = db.query(Parent).filter(Parent.parent_id == parent_id).first()
#         if not parent:
#             raise HTTPException(status_code=404, detail=f"Parent with ID {parent_id} not found")

#         if new_password != confirm_new_password:
#             raise HTTPException(status_code=400, detail="New passwords do not match")

#         if not bcrypt.checkpw(current_password.encode('utf-8'), parent.p_password.encode('utf-8')):
#             raise HTTPException(status_code=400, detail="Wrong current password")

#         if not validate_password(new_password):
#             raise HTTPException(status_code=400, detail="Invalid new password")

#         hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
#         parent.p_password = hashed_new_password
#         parent.p_password = hashed_new_password

#         db.commit()
#         contact = "900-417-3181"
#         email_contact = "vinay@example.com"

#         reset_email_body = f"""
#         <p>Dear User,</p>
#         <p>Your password has been successfully changed.</p>
#         <p>If you did not request this change, please contact support at {contact} or email us at {email_contact}.</p>
#         <p>Thank you!</p>
#         <br><br>
#         <p>Best regards,</p>
#         <p>Vinay Kumar</p>
#         <p>MaitriAI</p>
#         <p>900417181</p>
#         """
#         await send_email(
#             subject="Password Change Confirmation",
#             email_to=parent.primary_email,
#             body=reset_email_body
#         )
#         return {"message": "Password changed successfully"}

#     except HTTPException as e:
#         raise e

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
##################################################################################################################################
@router.post("/parent/", response_model=None)
def create_parent(parent: ParentCreate, db: Session = Depends(get_db)):
    db_parent = Parent(**parent.dict())
    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)
    return db_parent

@router.get("/student/{student_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_parent)])
def read_student_details(student_id: int, parent_id: int = Depends(get_user_id_from_token), db: Session = Depends(get_db)):
    # Fetch student details
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Fetch parent details
    parent = db.query(Parent).filter(Parent.parent_id == parent_id, Parent.student_id == student_id).first()
    if not parent:
        raise HTTPException(status_code=403, detail="Access denied. This student is not associated with the parent.")
    # Fetch parent details
   
    # Fetch course details
    course_details = db.query(CourseDetails).filter(CourseDetails.id == student.id).first()
    if course_details:
        course = db.query(Course).filter(Course.id == course_details.courses).first()
        standard = db.query(Standard).filter(Standard.id == course_details.standards).first()
        subject = db.query(Subject).filter(Subject.id == course_details.subjects).first()
        module = db.query(Module).filter(Module.id == course_details.modules).first()
    else:
        course = None
        standard = None
        subject = None
        module = None

    # Fetch payment details
    payment = db.query(Payment).filter(Payment.user_id == student.user_id).order_by(desc(Payment.created_on)).first()

    return {
        "student_id": student.id,
        "first_name": student.first_name,
        "middle_name": student.middle_name,
        "last_name": student.last_name,
        "date_of_birth": student.date_of_birth,
        "gender": student.gender,
        "nationality": student.nationality,
        "date_of_joining": student.date_of_joining,
        "date_of_completion": student.date_of_completion,
        "parent_details": {
            "parent_id": parent.parent_id if parent else None,
            "first_name": parent.p_first_name if parent else None,
            "middle_name": parent.p_middle_name if parent else None,
            "last_name": parent.p_last_name if parent else None,
            "guardian": parent.guardian if parent else None,
            "primary_no": parent.primary_no if parent else None,
            "primary_email": parent.primary_email if parent else None,
        },
        "course_details": {
            "course_name": course.name if course else None,
            "standard_name": standard.name if standard else None,
            "subject_name": subject.name if subject else None,
            "module_name": module.name if module else None,
        },
        "payment_details": {
            "payment_id": payment.payment_id if payment else None,
            "amount": payment.amount if payment else None,
            "payment_mode": payment.payment_mode if payment else None,
            "payment_info": payment.payment_info if payment else None,
            "other_info": payment.other_info if payment else None,
            "created_on": payment.created_on if payment else None,
        }
    }

@router.get("/parent/{parent_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_parent)])
def read_parent(parent_id: int, db: Session = Depends(get_db)):
    parent = db.query(Parent).filter(Parent.parent_id == parent_id).first()
    if parent is None:
        raise HTTPException(status_code=404, detail="Parent not found")
    return {
        "parent_id": parent.parent_id,
        "first_name": parent.p_first_name,
        "middle_name": parent.p_middle_name,
        "last_name": parent.p_last_name,
        "guardian": parent.guardian,
        "primary_no": parent.primary_no,
        "primary_email": parent.primary_email,
        "student_id":parent.student_id,
        "user_type":parent.user_type,
        # Add any other parent details needed
    }
# @router.get("/parent/", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_parent)])
# def read_all_parent(db: Session = Depends(get_db)):
#     parent = db.query(Parent).all()
#     if parent is None:
#         raise HTTPException(status_code=404, detail="Parent not found")
#     return parent

@router.get("/parent/", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_parent)])
def read_all_parent(db: Session = Depends(get_db)):
    parents = db.query(Parent).all()
    if not parents:
        raise HTTPException(status_code=404, detail="Parents not found")
    
    parent_data = [
        {
            "first_name": parent.p_first_name,
            "middle_name": parent.p_middle_name,
            "last_name": parent.p_last_name,
            "guardian": parent.guardian,
            "primary_no": parent.primary_no,
            "primary_email": parent.primary_email,
            "student_id": parent.student_id,
            "user_type": parent.user_type,
            # Add any other parent details needed
        }
        for parent in parents
    ]
    
    return parent_data


@router.put("/parent/{parent_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_parent)])
def update_parent(
    parent_id: int, parent: ParentCreate, db: Session = Depends(get_db)
):
    db_parent = (
        db.query(Parent).filter(Parent.parent_id == parent_id).first()
    )
    if db_parent is None:
        raise HTTPException(status_code=404, detail="Parent not found")
    update_data = parent.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_parent, key, value)
    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)
    return db_parent


# @router.delete("/parent/{parent_id}", response_model=None)
# def delete_parent(parent_id: int, db: Session = Depends(get_db)):
#     db_parent = (
#         db.query(Parent).filter(Parent.parent_id == parent_id).first()
#     )
#     if db_parent is None:
#         raise HTTPException(status_code=404, detail="Parent not found")
#     db.delete(db_parent)
#     db.commit()
#     return {"message": "parents info deleted successfully"}
############################################################################################################

@router.get("/announcement/{announcement_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_student_teacher_parent)])
async def get_announcement_parent(announcement_id: int, db: Session = Depends(get_db)):
    announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    base_url_path = "http://192.168.29.82:8001"  
    announcement_images_path = announcement.announcement_images
    if announcement_images_path:
        announcement_images_url = f"{base_url_path}/{announcement_images_path}"
    else:
        announcement_images_url = None

    announcement_response = Announcement(
        id=announcement.id,
        title=announcement.title,
        announcement_text=announcement.announcement_text,
        announcement_images=announcement_images_url
    )

    return announcement_response