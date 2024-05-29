# from fastapi import Depends, APIRouter, HTTPException
# from sqlalchemy.orm import Session
# from ..scheemas import DependentsBase, DependentsCreate,DependentsUpdate
# from db.session import get_db
# from ..Model.teacher_depends import Dependents
# from typing import List

# router = APIRouter()

# # Create dependent record
# @router.post("/dependents/", response_model=None)
# def create_dependent(dependent: DependentsCreate, employee_id: int, db: Session = Depends(get_db)):
#     db_dependent = Dependents( employee_id=employee_id, **dependent.dict())
#     db.add(db_dependent)
#     db.commit()
#     db.refresh(db_dependent)
#     return db_dependent

# # Read dependent record by ID
# @router.get("/dependents/{employee_id}", response_model=None)
# def read_dependent(employee_id: int, db: Session = Depends(get_db)):
#     dependent = db.query(Dependents).filter(Dependents.employee_id == employee_id).first()
#     if not dependent:
#         raise HTTPException(status_code=404, detail="Dependent not found")
#     return dependent

# # Update dependent record
# @router.put("/dependents/{employee_id}", response_model=None)
# def update_dependent(employee_id: int, dependent_update: DependentsUpdate, db: Session = Depends(get_db)):
#     db_dependent = db.query(Dependents).filter(Dependents.employee_id == employee_id).first()
#     if not db_dependent:
#         raise HTTPException(status_code=404, detail="Dependent not found")
#     for key, value in dependent_update.dict().items():
#         setattr(db_dependent, key, value)
#     db.commit()
#     db.refresh(db_dependent)
#     return db_dependent

# # Delete dependent record
# @router.delete("/dependents/{employee_id}")
# def delete_dependent(employee_id: int, db: Session = Depends(get_db)):
#     dependent = db.query(Dependents).filter(Dependents.employee_id == employee_id).first()
#     if not dependent:
#         raise HTTPException(status_code=404, detail="Dependent not found")
#     db.delete(dependent)
#     db.commit()
#     return {"message": "Dependent deleted successfully"}
