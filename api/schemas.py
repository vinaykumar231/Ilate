from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile, File
from datetime import date
from enum import Enum


#######################Company################################
class CompanyCreate(BaseModel):
    name: str


class CompanyUpdate(BaseModel):
    name: str


####################Branch#######################################
class BranchCreate(BaseModel):
    name: str


class BranchUpdate(BaseModel):
    name: str


###################Designation###################################
class DesignationCreate(BaseModel):
    name: str


class DesignationUpdate(BaseModel):
    name: str


####################Module#########################################
class ModuleCreate(BaseModel):
    name: str


class ModuleUpdate(BaseModel):
    name: str


#####################Usertype#######################################
class UserTypeCreate(BaseModel):
    name: str


class UserTypeUpdate(BaseModel):
    name: str


####################Student###########################################
class StudentBase(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    date_of_birth: date
    gender: str
    nationality: str
    referral: str
    date_of_joining: date
    date_of_completion: Optional[date] = None
    # id_proof: UploadFile = File(..., description="Upload ID Proof")
    # address_proof: UploadFile = File(..., description="Upload Address Proof")


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    nationality: Optional[str] = None
    referral: Optional[str] = None
    date_of_joining: Optional[date] = None
    date_of_completion: Optional[date] = None


class Student(StudentBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

##############################CoureDetails########################
from pydantic import BaseModel

class CourseDetailsCreate(BaseModel):
    subject: str
    standard: str
    module: str
    course: str

class CourseDetailsUpdate(BaseModel):
    subject: str
    standard: str
    module: str
    course: str


##################################user#############################
class LoginInput(BaseModel):
    email: str
    user_password: str


class ChangePassword(BaseModel):
    current_password: str
    new_password: str

    class Config:
        from_attributes = True


class UserType(str, Enum):
    admin = "admin"
    student = "student"
    teacher = "teacher"
    user = "user"


class UserCreate(BaseModel):
    user_name: str
    user_email: str
    user_password: str
    user_type: UserType = UserType.user
    phone_no: str

    class Config:
        from_attributes = True


class UpdateUser(BaseModel):
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    phone_no: Optional[int] = None
    user_type: Optional[str] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None


################################DemoFormFill###############################
class DemoformfillCreate(BaseModel):
    user_id: int
    name: str
    email_id: str
    contact_no: str
    standard: str
    course: str
    school: str
    teaching_mode: str
    other_info: str


class DemoformfillResponse(BaseModel):
    FormID: int
    GuestId: int
    Name: str
    EmailId: str
    ContactNo: str
    Standard: str
    Course: str
    School: str
    TeachingMode: str
    OtherInfo: str


##############################Parent#################################
class ParentBase(BaseModel):
    p_first_name: str
    p_middle_name: Optional[str]
    p_last_name: str
    guardian: str
    primary_no: str
    secondary_no: Optional[str]
    primary_email: str
    secondary_email: Optional[str]


class ParentCreate(ParentBase):
    pass


class ParentInfoUpdate(ParentBase):
    p_first_name: Optional[str] = None
    p_middle_name: Optional[str] = None
    p_last_name: Optional[str] = None
    guardian: Optional[str] = None
    primary_no: Optional[str] = None
    secondary_no: Optional[str] = None
    primary_email: Optional[str] = None
    secondary_email: Optional[str] = None


class Parent(ParentBase):
    parent_id: int
    student_id: int

    class Config:
        orm_mode = True


#########################studentContact#####################################
class StudentContactBase(BaseModel):
    primary_no: str
    secondary_no: Optional[str]
    primary_email: str
    secondary_email: Optional[str]
    current_address: str
    permanent_address: str


class StudentContactCreate(StudentContactBase):
    pass


class StudentContactUpdate(StudentContactBase):
    primary_no: Optional[str] = None
    secondary_no: Optional[str] = None
    primary_email: Optional[str] = None
    secondary_email: Optional[str] = None
    current_address: Optional[str] = None
    permanent_address: Optional[str] = None


class StudentContact(StudentContactBase):
    student_id: int

    class Config:
        orm_mode = True


#######################StudentEducation######################################
class PreEducationBase(BaseModel):
    student_class: str
    school: str
    year_of_passing: int
    percentage: float


class PreEducationCreate(PreEducationBase):
    pass


class PreEducationUpdate(PreEducationBase):
    student_class: Optional[str] = None
    school: Optional[str] = None
    year_of_passing: Optional[int] = None
    percentage: Optional[float] = None


class PreEducation(PreEducationBase):
    id: int
    student_id: int

    class Config:
        orm_mode = True


############# courses ########################################################


class CourseBase(BaseModel):
    name: str


class CourseCreate(CourseBase):
    pass


################## subjects ################################################

class SubjectBase(BaseModel):
    name: str


class SubjectCreate(SubjectBase):
    pass


#############################Standard##########################################
class StandardBase(BaseModel):
    name: str


class StandardCreate(StandardBase):
    pass


##############################DemoVideo############################################
# class DemoVideoCreate(BaseModel):
#     title: str
#     url: str
#     course_id: int
#     subject_id: int
#     standard_id: int

class VideoBase(BaseModel):
    name: str
    url: str


class VideoCreate(VideoBase):
    pass


class Video(VideoBase):
    id: int
    course_id: int
    standard_id: int
    subject_id: int

    class Config:
        orm_mode = True


######################################Inquiry##################################################
class InquiryCreate(BaseModel):
    name: str
    email: str
    phone: str
    message: str
