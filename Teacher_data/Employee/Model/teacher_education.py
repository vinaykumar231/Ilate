# from sqlalchemy import Column, String, Integer, Float, ForeignKey
# from sqlalchemy.orm import relationship
# from db.base import Base
# from ..Model.employee_master_table import Employee


# class Education(Base):
#     __tablename__ = "education"

#     id = Column(Integer, primary_key=True, index=True)
#     employee_id = Column(Integer, ForeignKey("employee.employee_id"), index=True)
#     education_level = Column(String(length=50))
#     institution = Column(String(length=50))
#     specialization = Column(String(length=50))
#     field_of_study = Column(String(length=50))
#     year_of_passing = Column(Integer)
#     percentage = Column(Float)


#     # Define many-to-one relationship with Employee
#     employee = relationship("Employee", back_populates="educations")

   

