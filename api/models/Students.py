from sqlalchemy import Column, Integer, String, Date, ForeignKey
from db.base import Base
from sqlalchemy.orm import relationship

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    first_name = Column(String(255))
    middle_name = Column(String(255), nullable=True)
    last_name = Column(String(255))
    date_of_birth = Column(Date)
    gender = Column(String(255))
    nationality = Column(String(255))
    referral = Column(String(255))
    date_of_joining = Column(Date)
    date_of_completion = Column(Date, nullable=True)
    # id_proof = Column(String(255))
    # address_proof = Column(String(255))

    # Define one-to-one relationship with ContactInformation
    contact_info = relationship("ContactInformation", uselist=False, back_populates="student")

    # Define one-to-many relationship with PreEducation
    pre_education = relationship("PreEducation", uselist=False,  back_populates="student")

    # Define one-to-one relationship with Parent
    parent_info = relationship("Parent", uselist=False, back_populates="student")

    course_details = relationship("CourseDetails", uselist=False, back_populates="student")
