from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from auth.auth_bearer import JWTBearer,get_admin
from ..models import Inquiry
from ..schemas import InquiryCreate



router = APIRouter()


@router.post("/inquiries/", response_model=None)
async def create_inquiry(inquiry: InquiryCreate, db: Session = Depends(get_db)):
    db_inquiry = Inquiry(**inquiry.dict())
    db.add(db_inquiry)
    db.commit()
    db.refresh(db_inquiry)
    return db_inquiry

@router.get("/get_inquiries/", response_model= None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def get_inquiries(db: Session = Depends(get_db)):
    return db.query(Inquiry).all()


