# from sqlalchemy import select, Column, Integer, String, ForeignKey, Float, JSON
# from db.base import Base
# from sqlalchemy.orm import Session
# from sqlalchemy.orm import relationship


# class Fee(Base):
#     __tablename__ = "fees"

#     id = Column(Integer, primary_key=True, index=True)
#     course_id = Column(Integer, ForeignKey('courses.course_id'))
#     year = Column(Integer)
#     subject_id = Column(Integer, ForeignKey('subjects.subject_id'))
#     modules_enrolled = Column(Integer)
#     batchid = Column(Integer, ForeignKey('batches.batchid'))
#     total_amount = Column(Float)
#     installment_number = Column(Integer)
#     installments = Column(JSON)
    
#     @staticmethod
#     def get_amount_by_criteria(course_id: int, year: int, subject_id: int, modules_enrolled: int, batchid: int, db: Session) -> float:
#         query = select(Fees.amount).filter(
#             Fees.course_id == course_id,
#             Fees.year == year,
#             Fees.subject_id == subject_id,
#             Fees.modules_enrolled == modules_enrolled,
#             Fees.batchid == batchid
#         )
#         result = db.execute(query).fetchone()
#         if result:
#             return result[0]  # Return the amount
#         else:
#             return None  # Or handle accordingly if no result found

#     # Relationships
#     course = relationship("Course", back_populates="fees")
#     subject = relationship("Subject", back_populates="fees")
#     batch = relationship("Batch", back_populates="fees")
