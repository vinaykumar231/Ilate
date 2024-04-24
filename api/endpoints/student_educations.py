from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from ..models import PreEducation
from ..schemas import PreEducationCreate

router = APIRouter()


@router.post("/preeducation/", response_model=None)
def create_preeducation(preeducation: PreEducationCreate, db: Session = Depends(get_db)):
    db_preeducation = PreEducation(**preeducation.dict())
    db.add(db_preeducation)
    db.commit()
    db.refresh(db_preeducation)
    return db_preeducation


@router.get("/preeducation/{student_id}", response_model=None)
def read_preeducation(student_id: int, db: Session = Depends(get_db)):
    db_preeducation = (
        db.query(PreEducation).filter(PreEducation.StudentID == student_id).first()
    )
    if db_preeducation is None:
        raise HTTPException(status_code=404, detail="PreEducation not found")
    return db_preeducation


@router.get("/preeducations/", response_model=None)
def read_preeducations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(PreEducation).offset(skip).limit(limit).all()


@router.put("/preeducation/{student_id}", response_model=None)
def update_preeducation(student_id: int, preeducation: PreEducationCreate, db: Session = Depends(get_db)):
    db_preeducation = (
        db.query(PreEducation).filter(PreEducation.StudentID == student_id).first()
    )
    if db_preeducation is None:
        raise HTTPException(status_code=404, detail="PreEducation not found")
    update_data = preeducation.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_preeducation, key, value)
    db.add(db_preeducation)
    db.commit()
    db.refresh(db_preeducation)
    return db_preeducation


@router.delete("/preeducation/{student_id}", response_model=None)
def delete_preeducation(student_id: int, db: Session = Depends(get_db)):
    db_preeducation = (
        db.query(PreEducation).filter(PreEducation.StudentID == student_id).first()
    )
    if db_preeducation is None:
        raise HTTPException(status_code=404, detail="PreEducation not found")
    db.delete(db_preeducation)
    db.commit()
    return db_preeducation
