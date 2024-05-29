# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
# from sqlalchemy.orm import relationship
# from db.base import Base
# from datetime import datetime, timezone

# class PaymentStatus(Base):
#     __tablename__ = "payment_status"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.user_id"))
#     status = Column(String(50), index=True)
#     amount = Column(Integer)
#     charge_id = Column(String(100))
#     created_at = Column(DateTime, default=datetime.now(timezone.utc))

#     # Define relationship with users table
#     user = relationship("LmsUsers", back_populates="payments")
