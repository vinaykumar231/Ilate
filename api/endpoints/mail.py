from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from ..models.mail import Mail
from pydantic import BaseModel, Field
from ..schemas import  MailCreate
from datetime import datetime
import pytz


router = APIRouter()

# ------------------------------------------------------------------------------------------------------------------
                        #mail
# ------------------------------------------------------------------------------------------------------------------

@router.post("/mail/", response_model=None)
def create_mail(mail: MailCreate, db: Session = Depends(get_db)):
    db_mail = Mail(**mail.dict())
    utc_now = pytz.utc.localize(datetime.utcnow())
    ist_now = utc_now.astimezone(pytz.timezone('Asia/Kolkata'))
    db_mail.created_on = ist_now
    db.add(db_mail)
    db.commit()
    db.refresh(db_mail)
    return db_mail

@router.get("/mail/", response_model=None)
def read_all_mails(db: Session = Depends(get_db)):
    return db.query(Mail).all()

@router.get("/mail/{mail_id}", response_model=None)
def read_mail(mail_id: int, db: Session = Depends(get_db)):
    db_mail = db.query(Mail).filter(Mail.id == mail_id).first()
    if db_mail is None:
        raise HTTPException(status_code=404, detail="Mail not found")
    return db_mail

@router.put("/mail/{mail_id}", response_model=None)
def update_mail(mail_id: int, mail: MailCreate, db: Session = Depends(get_db)):
    db_mail = db.query(Mail).filter(Mail.id == mail_id).first()
    if db_mail is None:
        raise HTTPException(status_code=404, detail="Mail not found")
    for key, value in mail.dict().items():
        setattr(db_mail, key, value)
    db.commit()
    db.refresh(db_mail)
    return db_mail

@router.delete("/mail/{mail_id}", response_model=None)
def delete_mail(mail_id: int, db: Session = Depends(get_db)):
    db_mail = db.query(Mail).filter(Mail.id == mail_id).first()
    if db_mail is None:
        raise HTTPException(status_code=404, detail="Mail not found")
    db.delete(db_mail)
    db.commit()
    return {"message": "mail deleted successfully"}