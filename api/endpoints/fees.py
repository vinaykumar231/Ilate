from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from typing import List
from sqlalchemy.orm import Session
from db.session import get_db
from ..models import Fee, Course, Standard, Subject, Module, Batch
from ..schemas import FeeCreate, FeeUpdate
from auth.auth_bearer import JWTBearer, get_admin, get_teacher, get_admin_or_teacher, get_admin_or_student

router = APIRouter()

@staticmethod
def get_amount_by_criteria(
    course_id: int, standard_id: int, year: int, subject_id: int, module_id: int, batch_id: int, db: Session
) -> float:
    try:
        course = db.query(Course).filter_by(id=course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail=f"Course with id {course_id} not found")

        standard = db.query(Standard).filter_by(id=standard_id).first()
        if not standard:
            raise HTTPException(status_code=404, detail=f"Standard with id {standard_id} not found")

        subject = db.query(Subject).filter_by(id=subject_id).first()
        if not subject:
            raise HTTPException(status_code=404, detail=f"Subject with id {subject_id} not found")

        module = db.query(Module).filter_by(id=module_id).first()
        if not module:
            raise HTTPException(status_code=404, detail=f"Module with id {module_id} not found")

        batch = db.query(Batch).filter_by(id=batch_id).first()
        if not batch:
            raise HTTPException(status_code=404, detail=f"Batch with id {batch_id} not found")

        query = select(Fee.amount).filter(
            Fee.course_id == course_id,
            Fee.standard_id == standard_id,
            Fee.year == year,
            Fee.subject_id == subject_id,
            Fee.module_id == module_id,
            Fee.batch_id == batch_id
        )
        result = db.execute(query).fetchone()
        if result:
            return {"amount":result[0]}
        else:
            raise HTTPException(status_code=404, detail="No record found with the given criteria")
    except HTTPException as e:
        raise e

        

# Create a new fee
@router.post("/fees/create_fees/", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_student)])
async def create_fee(fee_data: FeeCreate, db: Session = Depends(get_db)):
    try:
        related_entities = [
            (Course, fee_data.course_id, "Course"),
            (Subject, fee_data.subject_id, "Subject"),
            (Standard, fee_data.standard_id, "Standard"),
            (Module, fee_data.module_id, "Module"),
            (Batch, fee_data.batch_id, "Batch")
        ]

        for entity_cls, entity_id, entity_name in related_entities:
            entity_exists = db.query(entity_cls).filter(entity_cls.id == entity_id).first()
            if not entity_exists:
                raise HTTPException(status_code=404, detail=f"{entity_name} with id {entity_id} not found")

        fee = Fee(**fee_data.dict())
        db.add(fee)
        db.commit()
        db.refresh(fee)
        return fee
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert fees: {str(e)}")

@router.get("/fees/bycriteria", response_model=None)
async def read_fees(
    course_id: int = None, standard_id: int = None, year: int = None, subject_id: int = None,
    module_id: int = None, batch_id: int = None, db: Session = Depends(get_db)
):
    return get_amount_by_criteria(course_id, standard_id, year, subject_id, module_id, batch_id, db)


# Get all fees
@router.get("/fees/all_fees/", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def read_fees(db: Session = Depends(get_db)):
    try:
        return db.query(Fee).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch fees: {str(e)}")

# Get a specific fee by ID
@router.get("/fees/{fee_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def read_fee(fee_id: int, db: Session = Depends(get_db)):
    try:
        fee = db.query(Fee).filter(Fee.id == fee_id).first()
        if fee is None:
            raise HTTPException(status_code=404, detail="Fee not found")
        return fee
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch fees: {str(e)}")

# Update a fee by ID
@router.put("/fees/update_fees/{fee_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def update_fee(fee_id: int, fee_data: FeeUpdate, db: Session = Depends(get_db)):
    try:
        fee = db.query(Fee).filter(Fee.id == fee_id).first()
        if fee is None:
            raise HTTPException(status_code=404, detail="Fee not found")
        for key, value in fee_data.dict().items():
            setattr(fee, key, value)
        db.commit()
        db.refresh(fee)
        return fee
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update fees: {str(e)}")

# Delete a fee by ID
@router.delete("/fees/delete_fees/{fee_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def delete_fee(fee_id: int, db: Session = Depends(get_db)):
    try:
        fee = db.query(Fee).filter(Fee.id == fee_id).first()
        if fee is None:
            raise HTTPException(status_code=404, detail="fee not found")
        db.delete(fee)
        db.commit()
        return fee
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete fees: {str(e)}")