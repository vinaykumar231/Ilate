from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from db.base import Base
# from .Teacher import Teacher
# from .course import Course

class TeacherCourse(Base):
    __tablename__ = "teacher_courses"

    id = Column(Integer, primary_key=True, index=True )
    teacher_id = Column(Integer, ForeignKey("teachers.Teacher_id"))
    course_id = Column(Integer, ForeignKey("courses.id"))

    teacher_Assign = relationship("Teacher", back_populates="courses_by")
    course_Assign = relationship("Course", back_populates="teacher_by")