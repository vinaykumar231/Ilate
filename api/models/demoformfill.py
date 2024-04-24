from sqlalchemy import Column, Integer, String, ForeignKey
from db.base import Base
from sqlalchemy.orm import relationship


class DemoFormFill(Base):
    __tablename__ = "demoformfill"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    name = Column(String(255), index=True)
    email_id = Column(String(255), index=True)
    contact_no = Column(String(255), index=True)
    standard = Column(String(255), index=True)
    course = Column(String(255), index=True)
    school = Column(String(255), index=True)
    teaching_mode = Column(String(255), index=True)
    other_info = Column(String(255), index=True)

    demo = relationship("LmsUsers", back_populates="demos", uselist=False, primaryjoin="DemoFormFill.user_id==LmsUsers.user_id")


