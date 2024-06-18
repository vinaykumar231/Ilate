from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.session import get_db
from ..models import Batch
from ..schemas import BatchCreate, BatchUpdate
from auth.auth_bearer import JWTBearer, get_admin, get_teacher, get_admin_or_teacher

router = APIRouter()



# Create a new Batch
@router.post("/batches/", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def create_batch(batch_data: BatchCreate, db: Session = Depends(get_db)):
    batch = Batch(**batch_data.dict())
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch

# Get all batches
@router.get("/batches/", response_model=None)
async def read_all_batches(db: Session = Depends(get_db)):
    return db.query(Batch).all()

# Get a specific batch by ID
@router.get("/batches/{batch_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def read_batch(batch_id: int, db: Session = Depends(get_db)):
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")
    return batch

# Update a batch by ID
@router.put("/batches/{batch_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def update_batch(batch_id: int, batch_data: BatchUpdate, db: Session = Depends(get_db)):
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")
    for key, value in batch_data.dict().items():
        setattr(batch, key, value)
    db.commit()
    db.refresh(batch)
    return batch

# Delete a batch by ID
@router.delete("/batches/{batch_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def delete_batch(batch_id: int, db: Session = Depends(get_db)):
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if batch is None:
        raise HTTPException(status_code=404, detail="batch not found")
    db.delete(batch)
    db.commit()
    return {"detail": "Batch deleted successfully"}
