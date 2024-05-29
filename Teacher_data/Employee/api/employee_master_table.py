# from fastapi import Depends, APIRouter, HTTPException
# from sqlalchemy.orm import Session
# from ..scheemas import EmployeeBase,EmployeeCreate,EmployeeUpdate
# from db.session import get_db
# from ..Model.employee_master_table import Employee
# from typing import List


# router = APIRouter()

# # Create employee record
# @router.post("/employees/", response_model=None)
# def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
#     db_employee = Employee(**employee.dict())
#     db.add(db_employee)
#     db.commit()
#     db.refresh(db_employee)
#     return db_employee

# # Read employee record by ID
# @router.get("/employees/{employee_id}", response_model=None)
# def read_employee(employee_id: int, db: Session = Depends(get_db)):
#     employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
#     if not employee:
#         raise HTTPException(status_code=404, detail="Employee not found")
#     return employee

# # Update employee record
# @router.put("/employees/{employee_id}", response_model=None)
# def update_employee(employee_id: int, employee_update: EmployeeUpdate, db: Session = Depends(get_db)):
#     db_employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
#     if not db_employee:
#         raise HTTPException(status_code=404, detail="Employee not found")
#     for key, value in employee_update.dict().items():
#         setattr(db_employee, key, value)
#     db.commit()
#     db.refresh(db_employee)
#     return db_employee

# # Delete employee record
# @router.delete("/employees/{employee_id}")
# def delete_employee(employee_id: int, db: Session = Depends(get_db)):
#     employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
#     if not employee:
#         raise HTTPException(status_code=404, detail="Employee not found")
#     db.delete(employee)
#     db.commit()
#     return {"message": "Employee deleted successfully"}
