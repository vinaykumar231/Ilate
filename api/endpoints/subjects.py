from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.session import get_db
from ..models import Subject
from ..schemas import SubjectCreate
from auth.auth_bearer import JWTBearer, get_user_id_from_token

router = APIRouter()


@router.post("/subjects/", response_model=None)
def create_subject(subject: SubjectCreate, db: Session = Depends(get_db)):
    db_subject = Subject(**subject.dict())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

@router.get("/subjects/", response_model=None)
def read_subjects(db: Session = Depends(get_db)):
    return db.query(Subject).all()

@router.get("/subjects/{subject_id}", response_model=None)
def read_subject(subject_id: int, db: Session = Depends(get_db)):
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return db_subject

@router.put("/subjects/{subject_id}", response_model=None)
def update_subject(subject_id: int, subject: SubjectCreate, db: Session = Depends(get_db)):
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    db_subject.name = subject.name
    db_subject.course_id = subject.course_id
    db.commit()
    db.refresh(db_subject)
    return db_subject

@router.delete("/subjects/{subject_id}", response_model=None)
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    db.delete(db_subject)
    db.commit()
    return db_subject
