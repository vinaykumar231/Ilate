# from sqlalchemy import Column, String, Integer, ForeignKey, Date
# from sqlalchemy.orm import relationship  # Import relationship from sqlalchemy.orm
# from db.base import Base
# from ..Model.employee_master_table import Employee


# class Dependents(Base):
#     __tablename__ = "dependents"

#     id = Column(Integer, primary_key=True, index=True)
#     employee_id = Column(Integer, ForeignKey("employee.employee_id"))
#     dependent_name = Column(String(length=50))
#     realtion = Column(String(length=50))
#     date_of_birth = Column(Date)

#     # Define many-to-one relationship with Employee
#     employee = relationship("Employee", back_populates="dependents")