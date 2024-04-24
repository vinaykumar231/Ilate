from fastapi import APIRouter, Depends, HTTPException
from ..models import Parent
from ..schemas import ParentCreate
from sqlalchemy.orm import Session
from db.session import get_db

router = APIRouter()


@router.post("/parent/", response_model=None)
def create_parent(parent: ParentCreate, db: Session = Depends(get_db)):
    db_parent = Parent(**parent.dict())
    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)
    return db_parent


@router.get("/parent/{parent_id}", response_model=None)
def read_parent(parent_id: int, db: Session = Depends(get_db)):
    db_parent = db.query(Parent).filter(Parent.ParentID == parent_id).first()
    if db_parent is None:
        raise HTTPException(status_code=404, detail="Parent not found")
    return db_parent


@router.get("/parents/", response_model=None)
def read_parents(db: Session = Depends(get_db)):
    return db.query(Parent).all()


@router.put("/parent/{parent_id}", response_model=None)
def update_parent(
    parent_id: int, parent: ParentCreate, db: Session = Depends(get_db)
):
    db_parent = (
        db.query(Parent).filter(Parent.ParentID == parent_id).first()
    )
    if db_parent is None:
        raise HTTPException(status_code=404, detail="Parent not found")
    update_data = parent.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_parent, key, value)
    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)
    return db_parent


@router.delete("/parent/{parent_id}", response_model=None)
def delete_parent(parent_id: int, db: Session = Depends(get_db)):
    db_parent = (
        db.query(Parent).filter(Parent.ParentID == parent_id).first()
    )
    if db_parent is None:
        raise HTTPException(status_code=404, detail="Parent not found")
    db.delete(db_parent)
    db.commit()
    return db_parent
