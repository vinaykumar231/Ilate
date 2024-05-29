# from fastapi import Depends, APIRouter, HTTPException
# from sqlalchemy.orm import Session
# from ..scheemas import EmergencyContactBase,EmergencyContactCreate,EmergencyContactUpdate
# from ..Model.teacher_emergency_contact import EmergencyContact
# from db.session import get_db
# from typing import List


# router = APIRouter()

# # Create emergency contact record
# @router.post("/emergency_contacts/", response_model=None)
# def create_emergency_contact(emergency_contact: EmergencyContactCreate, employee_id: int,  db: Session = Depends(get_db)):
#     db_emergency_contact = EmergencyContact( employee_id=employee_id, **emergency_contact.dict())
#     db.add(db_emergency_contact)
#     db.commit()
#     db.refresh(db_emergency_contact)
#     return db_emergency_contact


# # Read emergency contact record by ID
# @router.get("/emergency_contacts/{employee_id}", response_model=None)
# def read_emergency_contact(employee_id: int, db: Session = Depends(get_db)):
#     emergency_contact = db.query(EmergencyContact).filter(EmergencyContact.employee_id ==employee_id).first()
#     if not emergency_contact:
#         raise HTTPException(status_code=404, detail="Emergency contact not found")
#     return emergency_contact

# # Update emergency contact record
# @router.put("/emergency_contacts/{employee_id}", response_model=None)
# def update_emergency_contact(employee_id: int, emergency_contact_update: EmergencyContactUpdate, db: Session = Depends(get_db)):
#     db_emergency_contact = db.query(EmergencyContact).filter(EmergencyContact.employee_id == employee_id).first()
#     if not db_emergency_contact:
#         raise HTTPException(status_code=404, detail="Emergency contact not found")
#     for key, value in emergency_contact_update.dict().items():
#         setattr(db_emergency_contact, key, value)
#     db.commit()
#     db.refresh(db_emergency_contact)
#     return db_emergency_contact

# # Delete emergency contact record
# @router.delete("/emergency_contacts/{employee_id}")
# def delete_emergency_contact(employee_id: int, db: Session = Depends(get_db)):
#     emergency_contact = db.query(EmergencyContact).filter(EmergencyContact.employee_id == employee_id).first()
#     if not emergency_contact:
#         raise HTTPException(status_code=404, detail="Emergency contact not found")
#     db.delete(emergency_contact)
#     db.commit()
#     return {"message": "Emergency contact deleted successfully"}
