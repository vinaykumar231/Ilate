# from sqlalchemy import Column, String, Integer, Date, ForeignKey
# from db.base import Base
# from sqlalchemy.orm import relationship
# from ..Model.manager import Manager
# #from ..Model.teacher_contact_info import ContactInformation

# class Employee(Base):
#     __tablename__ = "employee"
#     employee_id = Column(Integer, primary_key=True)
#     f_name = Column(String(length=20), index=True)
#     m_name = Column(String(length=20), index=True)
#     l_name = Column(String(length=20), index=True)
#     dob = Column(Date)
#     gender = Column(String(length=10))
#     nationality = Column(String(length=20))
#     marital_status = Column(String(length=20))
#     citizenship_status = Column(String(length=20))
#     date_of_hire = Column(Date, nullable=True)
#     date_of_termination = Column(Date, nullable=True)
#     manager_id = Column(Integer, ForeignKey("manager.manager_id"), nullable=True)

#     # Define one-to-one relationship with ContactInformation
#     contact_information = relationship("TeacherContact", back_populates="employee")
    
#     educations = relationship("Education", back_populates="employee")

#     dependents = relationship("Dependents", back_populates="employee")

#     emergency_contacts1 = relationship("EmergencyContact", back_populates="employee1")

#     skills = relationship("Skill", back_populates="employee")

#     languages_spoken = relationship("LanguagesSpoken", back_populates="employee")

#     manager = relationship("Manager", back_populates="employee")




  