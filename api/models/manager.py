# from sqlalchemy import Column, String, Integer
# from db.base import Base
# from sqlalchemy.orm import relationship
# #from ..Model.employee_master_table import Employee

# class Manager(Base):
#     __tablename__ = "manager"

#     manager_id = Column(Integer, primary_key=True)
#     name = Column(String(length=20), index=True)
#     gender = Column(String(length=10))
#     department = Column(String(length=50))

#     employee = relationship("Employee", back_populates="manager")

