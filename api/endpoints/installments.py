from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
from ..models.installment import Installment
from ..models import Payment
from ..schemas import PaymentDetails, InstallmentResponse
from datetime import datetime, timedelta
from math import ceil, floor
import json
#from ..models.installment import InstallmentDetail

router = APIRouter()

# ------------------------------------------------------------------------------------------------------------------
                        #Installment
# ------------------------------------------------------------------------------------------------------------------

def calculate_installments(total_amount: float, installment_number: int) -> List[float]:
    installment_amount = total_amount / installment_number
    installment_amount = floor(installment_amount)
    installments = [installment_amount] * installment_number
    return installments

def calculate_due_dates(installment_number: int) -> List[str]:
    current_date = datetime.now()
    due_dates = [(current_date + timedelta(days=i*30)).strftime('%Y-%m-%d') for i in range(1, installment_number+1)]
    return due_dates

@router.post("/installments/Insert/", response_model=None)
async def post_payment_details(payment_id: int, total_amount: float, installment_number: int, db: Session = Depends(get_db)):
    try:
   
        existing_payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
        if not existing_payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        if total_amount <= 0 or installment_number <= 0:
            raise HTTPException(status_code=400, detail="Total amount and installment number must be positive")

        installments = calculate_installments(total_amount, installment_number)
        due_dates = calculate_due_dates(installment_number)
        
        installments_and_due_dates = [{"amount": amount, "due_date": date} for amount, date in zip(installments, due_dates)]
        
        installments_json = json.dumps(installments_and_due_dates)

        installment = Installment(payment_id=payment_id, total_amount=total_amount, installment_number=installment_number, installments=installments_json)
        db.add(installment)
        db.commit()
        db.refresh(installment)
        db.close()
        
        return installment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert installment: {str(e)}")


@router.get("/installments/Fetch/{installment_id}", response_model=None)
async def get_installment(installment_id: int, db: Session = Depends(get_db)):
    try:
        installment = db.query(Installment).filter(Installment. installment_id== installment_id).all()
        if not installment:
            raise HTTPException(status_code=404, detail="Installment not found")
        return installment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch installment: {str(e)}")

@router.put("/installments/Update/{installment_id}", response_model=None)
async def update_installment(installment_id: int, total_amount: float, installment_number: int, db: Session = Depends(get_db)):
   
    installment = db.query(Installment).filter(Installment.installment_id == installment_id).first()
    if not installment:
        raise HTTPException(status_code=404, detail="Installment not found")

    installments = calculate_installments(total_amount, installment_number)
    due_dates = calculate_due_dates(installment_number)

    installments_and_due_dates = [{"amount": amount, "due_date": date} for amount, date in zip(installments, due_dates)]

    installments_json = json.dumps(installments_and_due_dates)
    try:
        installment.total_amount = total_amount
        installment.installment_number = installment_number
        installment.installments = installments_json
        db.commit()
        db.refresh(installment)
    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail="An error occurred while updating the installment.") from e
    finally:
        db.close()  

    return installment
    
@router.delete("/installments/delete/{installment_id}")
async def delete_installment(installment_id: int, db: Session = Depends(get_db)):
    try:
        installments = db.query(Installment).filter(Installment.installment_id == installment_id).all()
        if not installments:
            raise HTTPException(status_code=404, detail=f"No installments found for payment_id: {installment_id}")
        
        for installment in installments:
            db.delete(installment)  

        db.commit()
        return {"All  data  have been deleted of  payment_id {installment_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete installment: {str(e)}")
