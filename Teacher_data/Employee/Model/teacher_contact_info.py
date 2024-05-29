# from sqlalchemy import Column, String, Integer, Date, ForeignKey
# from sqlalchemy.orm import Session, relationship
# from fastapi import HTTPException
# from db.base import Base
# from ..Model.employee_master_table import Employee

# #from my_config import api_respons


# class TeacherContact(Base):
#     __tablename__ = "teacher_contact_info"

#     # Define columns
#     employee_id = Column(Integer, ForeignKey("employee.employee_id"), primary_key=True, index=True)
#     primary_number = Column(String(length=50))
#     secondary_number = Column(String(length=50), nullable=True)
#     primary_email_id = Column(String(length=50))
#     secondary_email_id = Column(String(length=50), nullable=True)
#     current_address = Column(String(length=255))  
#     permanent_address = Column(String(length=255))  

#     # Define one-to-one relationship with Employee
#     employee = relationship("Employee", back_populates="contact_information")
