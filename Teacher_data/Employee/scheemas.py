# from pydantic import BaseModel
# from typing import Optional
# from pydantic import BaseModel, Field
# from datetime import date


# ######################### teacher contact info  #####################################

# class ContactInformationBase(BaseModel):
#     primary_number: str = Field(..., max_length=50)
#     secondary_number: str = Field(None, max_length=50)
#     primary_email_id: str = Field(..., max_length=50)
#     secondary_email_id: str = Field(None, max_length=50)
#     current_address: str = Field(..., max_length=255)
#     permanent_address: str = Field(..., max_length=255)

# class ContactInformationCreate(ContactInformationBase):
#     pass

# class ContactInformationUpdate(ContactInformationBase):
#     pass

# ######################### teacher education  #####################################

# class EducationBase(BaseModel):
#     education_level: str
#     institution: str
#     specialization: str
#     field_of_study: str
#     year_of_passing: int
#     percentage: float

# class EducationCreate(EducationBase):
#     pass

# class EducationUpdate(EducationBase):
#     pass

# ######################### teacher skills  #####################################
# class SkillBase(BaseModel):
#     skill: str
#     certification: str
#     license: str

# class SkillCreate(SkillBase):
#     pass

# class SkillUpdate(SkillBase):
#     pass

# ######################### teacher language knowledge  #####################################

# class LanguagesSpokenBase(BaseModel):
#     languages: str

# class LanguagesSpokenCreate(LanguagesSpokenBase):
#     pass

# class LanguagesSpokenUpdate(LanguagesSpokenBase):
#     pass

# ######################### teacher EmergencyContact #####################################

# class EmergencyContactBase(BaseModel):
#     emergency_contact_name: str
#     relation: str
#     emergency_contact_number: int

# class EmergencyContactCreate(EmergencyContactBase):
#     pass

# class EmergencyContactUpdate(EmergencyContactBase):
#     pass


######################### teacher depends #####################################
# class DependentsBase(BaseModel):
#     dependent_name: str
#     realtion: str
#     date_of_birth: date

# class DependentsCreate(DependentsBase):
#     pass

# class DependentsUpdate(DependentsBase):
#     pass

# ######################### Employee Master Table #####################################
# class EmployeeBase(BaseModel):
#     f_name: str
#     m_name: Optional[str]
#     l_name: str
#     dob: date
#     gender: str
#     nationality: str
#     marital_status: str
#     citizenship_status: str
#     date_of_hire: Optional[date]
#     date_of_termination: Optional[date]
#     manager_id: Optional[int]

# class EmployeeCreate(EmployeeBase):
#     pass

# class EmployeeUpdate(EmployeeBase):
#     pass


# ######################### Manager #####################################

# class ManagerBase(BaseModel):
#     name: str
#     gender: str
#     department: str

# class ManagerCreate(ManagerBase):
#     pass

# class ManagerUpdate(ManagerBase):
#     pass

# class ManagerInDBBase(ManagerBase):
#     manager_id: int

