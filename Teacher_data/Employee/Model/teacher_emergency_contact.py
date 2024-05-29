# from sqlalchemy import Column, String, Integer, ForeignKey
# from sqlalchemy.orm import relationship
# from db.base import Base
# from ..Model.employee_master_table import Employee


# class EmergencyContact(Base):
#     __tablename__ = "emergency_contact"

#     id = Column(Integer, primary_key=True, index=True)
#     employee_id = Column(Integer, ForeignKey("employee.employee_id"), index=True)
#     emergency_contact_name = Column(String(length=50))
#     relation = Column(String(length=50))
#     emergency_contact_number = Column(Integer)

#     # Define many-to-one relationship with Employee
#     employee1 = relationship(Employee, back_populates="emergency_contacts1")
