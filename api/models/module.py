from sqlalchemy import Column, Integer, String
from db.base import Base

class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
