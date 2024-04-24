from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from ..models import Standard
from ..schemas import StandardCreate

router = APIRouter()


@router.post("/standards/", response_model=None)
def create_standard(standard: StandardCreate, db: Session = Depends(get_db)):
    db_standard = Standard(**standard.dict())
    db.add(db_standard)
    db.commit()
    db.refresh(db_standard)
    return db_standard


@router.get("/standards/{standard_id}", response_model=None)
def read_standard(standard_id: int, db: Session = Depends(get_db)):
    db_standard = db.query(Standard).filter(Standard.id == standard_id).first()
    if db_standard is None:
        raise HTTPException(status_code=404, detail="Standard not found")
    return db_standard


@router.get("/standards/", response_model=None)
def read_standards(db: Session = Depends(get_db)):
    return db.query(Standard).all()


@router.put("/standards/{standard_id}", response_model=None)
def update_standard(standard_id: int, standard: StandardCreate, db: Session = Depends(get_db)):
    db_standard = db.query(Standard).filter(Standard.id == standard_id).first()
    if db_standard is None:
        raise HTTPException(status_code=404, detail="Standard not found")
    for attr, value in standard.dict().items():
        setattr(db_standard, attr, value)
    db.commit()
    db.refresh(db_standard)
    return db_standard


@router.delete("/standards/{standard_id}", response_model=None)
def delete_standard(standard_id: int, db: Session = Depends(get_db)):
    db_standard = db.query(Standard).filter(Standard.id == standard_id).first()
    if db_standard is None:
        raise HTTPException(status_code=404, detail="Standard not found")
    db.delete(db_standard)
    db.commit()
    return db_standard
