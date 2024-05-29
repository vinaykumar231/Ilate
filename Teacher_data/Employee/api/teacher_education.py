# from fastapi import Depends, APIRouter, HTTPException
# from sqlalchemy.orm import Session
# from ..scheemas import EducationBase,  EducationCreate,EducationUpdate
# from db.session import get_db
# from ..Model.teacher_education import Education
# from typing import List

# router = APIRouter()

# # Create education record
# @router.post("/education/", response_model=None)
# def create_education(education: EducationCreate, employee_id: int, db: Session = Depends(get_db)):
#     db_education = Education(  employee_id=employee_id, **education.dict())
#     db.add(db_education)
#     db.commit()
#     db.refresh(db_education)
#     return db_education


# # Read education record by ID
# @router.get("/education/{employee_id}", response_model=None)
# def read_education(employee_id: int, db: Session = Depends(get_db)):
#     education = db.query(Education).filter(Education.employee_id ==employee_id).first()
#     if not education:
#         raise HTTPException(status_code=404, detail="Education not found")
#     return education

# # Update education record
# @router.put("/education/{employee_id}", response_model=None)
# def update_education(employee_id: int, education_update: EducationUpdate, db: Session = Depends(get_db)):
#     db_education = db.query(Education).filter(Education.employee_id == employee_id).first()
#     if not db_education:
#         raise HTTPException(status_code=404, detail="Education not found")
#     for key, value in education_update.dict().items():
#         setattr(db_education, key, value)
#     db.commit()
#     db.refresh(db_education)
#     return db_education

# # Delete education record
# @router.delete("/education/{employee_id}")
# def delete_education(employee_id: int, db: Session = Depends(get_db)):
#     education = db.query(Education).filter(Education.employee_id == employee_id).first()
#     if not education:
#         raise HTTPException(status_code=404, detail="Education not found")
#     db.delete(education)
#     db.commit()
#     return {"message": "Education deleted successfully"}