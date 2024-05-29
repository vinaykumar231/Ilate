from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from auth.auth_bearer import JWTBearer,get_admin
from ..models import Inquiry
from ..schemas import InquiryCreate, InquiryUpdate
from datetime import datetime



router = APIRouter()


@router.post("/inquiries/", response_model=None)
async def create_inquiry(inquiry: InquiryCreate, db: Session = Depends(get_db)):
    try:
        db_inquiry = Inquiry(**inquiry.dict())
        db_inquiry.created_on = datetime.now()
        db.add(db_inquiry)
        db.commit()
        db.refresh(db_inquiry)
        return db_inquiry
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/get_inquiries/", response_model= None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def get_inquiries(db: Session = Depends(get_db)):
    return db.query(Inquiry).all()

@router.get("/inquiries/{inquiry_id}", response_model=None)
async def get_inquiry(inquiry_id: int, db: Session = Depends(get_db)):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return inquiry

@router.put("/inquiries/{inquiry_id}", response_model=None)
async def update_inquiry(inquiry_id: int, inquiry_update: InquiryUpdate, db: Session = Depends(get_db)):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    try:
        for key, value in inquiry_update.dict().items():
            setattr(inquiry, key, value)
        db.commit()
        db.refresh(inquiry)
        return inquiry
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/inquiries/{inquiry_id}", response_model=None)
async def delete_inquiry(inquiry_id: int, db: Session = Depends(get_db)):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    try:
        db.delete(inquiry)
        db.commit()
        return {"message": "Inquiry deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


