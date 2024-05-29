# from sqlalchemy import Column, String, Integer, ForeignKey
# from db.base import Base
# from sqlalchemy.orm import relationship
# from ..Model.employee_master_table import Employee


# class Skill(Base):
#     __tablename__ = "skills"

#     id = Column(Integer, primary_key=True, index=True)
#     employee_id = Column(Integer, ForeignKey("employee.employee_id"), index=True)
#     skill = Column(String(length=50))
#     certification = Column(String(length=50))
#     license = Column(String(length=50))

#     # Define many-to-one relationship with Employee
#     employee = relationship("Employee", back_populates="skills")
