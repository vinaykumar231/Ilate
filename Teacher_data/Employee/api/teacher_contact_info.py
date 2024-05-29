# from fastapi import Depends, APIRouter, HTTPException
# from sqlalchemy.orm import Session
# from ..scheemas import ContactInformationCreate, ContactInformationUpdate
# from db.session import get_db
# from ..Model.teacher_contact_info import TeacherContact
# from typing import List


# router = APIRouter()

# @router.post("/contact-info/",  response_model=None)
# def create_contact_info(contact_info: ContactInformationCreate, employee_id: int, db: Session = Depends(get_db)):
#     db_contact_info = TeacherContact(employee_id=employee_id, **contact_info.dict())
#     db.add(db_contact_info)
#     db.commit()
#     db.refresh(db_contact_info)
#     return db_contact_info

# @router.get("/contact-info/{employee_id}", response_model=None)
# def get_contact_info_by_id(employee_id: int, db: Session = Depends(get_db)):
#     contact_info = db.query(TeacherContact).filter(TeacherContact.employee_id == employee_id).first()
#     if contact_info is None:
#         raise HTTPException(status_code=404, detail="Contact information not found")
#     return contact_info

# @router.put("/contact-info/{employee_id}", response_model=None)
# def update_contact_info(employee_id: int, contact_info_update: ContactInformationUpdate, db: Session = Depends(get_db)):
#     db_contact_info = db.query(TeacherContact).filter(TeacherContact.employee_id == employee_id).first()
#     if db_contact_info is None:
#         raise HTTPException(status_code=404, detail="Contact information not found")
#     for key, value in contact_info_update.dict().items():
#         setattr(db_contact_info, key, value)
#     db.commit()
#     db.refresh(db_contact_info)
#     return db_contact_info

# @router.delete("/contact_info/{employee_id}", response_model=None)
# def delete_contact_info(employee_id: int, db: Session = Depends(get_db)):
#     contact_info = db.query(TeacherContact).filter(TeacherContact.employee_id == employee_id).first()
#     if contact_info is None:
#         raise HTTPException(status_code=404, detail="Contact information not found")
#     db.delete(contact_info)
#     db.commit()
#     return "teacher_contact deleted successfully"
