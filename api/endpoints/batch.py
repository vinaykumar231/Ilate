# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from typing import List
# from db.session import get_db
# from ..models.batch import Batch
# from ..schemas import BatchCreate
# from ..models import Fee

# router = APIRouter()

# # ------------------------------------------------------------------------------------------------------------------
#                         #Batch
# # ------------------------------------------------------------------------------------------------------------------

# @router.post("/batches/Insert/", response_model=None)
# def create_batch(batch: BatchCreate, db: Session = Depends(get_db)):
#     db_batch = Batch(**batch.dict())
#     db.add(db_batch)
#     db.commit()
#     db.refresh(db_batch)
#     return db_batch

# @router.get("/batches/Fetch/{batchid}", response_model=None)
# def read_batch(batchid: int, db: Session = Depends(get_db)):
#     batch = db.query(Batch).filter(Batch.batchid == batchid).first()
#     if not batch:
#         raise HTTPException(status_code=404, detail="Batch not found")
#     return batch

# @router.put("/batches/Update/{batchid}", response_model=None)
# def update_batch(batchid: int, batch: BatchCreate, db: Session = Depends(get_db)):
#     db_batch = db.query(Batch).filter(Batch.batchid == batchid).first()
#     if not db_batch:
#         raise HTTPException(status_code=404, detail="Batch not found")
#     for attr, value in batch.dict().items():
#         setattr(db_batch, attr, value)
#     db.commit()
#     db.refresh(db_batch)
#     return db_batch

# @router.delete("/batches/delete_batch/{batch_id}", response_model=None)
# async def delete_batch(batch_id: int, db: Session = Depends(get_db)):
#     batch = db.query(Batch).filter(Batch.id == batch_id).first()
#     if batch is None:
#         raise HTTPException(status_code=404, detail="Batch not found")
#     db.delete(batch)
#     db.commit()
#     return {"detail": "Batch deleted successfully"}
# # @router.get("/batches/", response_model=List[ BatchCreate])
# # def read_batches(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
# #     return db.query(Batch).offset(skip).limit(limit).all()
