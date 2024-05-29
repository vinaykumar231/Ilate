from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from ..models.payment import Payment
from ..models import Student, Course, LmsUsers, Batch,Module,Standard,Subject
from pydantic import BaseModel
from ..schemas import PaymentCreate,PaymentResponse
from auth.auth_bearer import JWTBearer, get_current_user, get_admin, get_admin_or_student
from typing import List
from sqlalchemy import desc
from datetime import datetime
from typing import Optional

router = APIRouter()

# ------------------------------------------------------------------------------------------------------------------
                        #Payments
# ------------------------------------------------------------------------------------------------------------------

@router.post("/payments/insert/", response_model=None)
def create_payment(
    payment: PaymentCreate, 
    db: Session = Depends(get_db), 
    current_user: LmsUsers = Depends(get_current_user)
):
    if not current_user.is_formsubmited:
        raise HTTPException(status_code=400, detail="Admission form not submitted")

    # Check if the payment has already been made based on the flag
    existing_payment = db.query(Payment).filter(Payment.user_id == current_user.user_id).first()
    
    
        # Check if the provided course, standard, subject, module, and batch exist in the database
    existing_course = db.query(Course).filter(Course.id == payment.course_id).first()
    existing_standard = db.query(Standard).filter(Standard.id == payment.standard_id).first()
    existing_subject = db.query(Subject).filter(Subject.id == payment.subject_id).first()
    existing_module = db.query(Module).filter(Module.id == payment.module_id).first()
    existing_batch = db.query(Batch).filter(Batch.id == payment.batch_id).first()  

    if not all([existing_course, existing_standard, existing_subject, existing_module, existing_batch]):
            raise HTTPException(status_code=404, detail="One or more of course, standard, subject, module, or batch not found")

        # Create the payment
    db_payment = Payment(
            user_id=current_user.user_id,
            course_id=payment.course_id,
            standard_id=payment.standard_id,
            subject_id=payment.subject_id,
            module_id=payment.module_id,
            batch_id=payment.batch_id,
            years=payment.years,
            amount=payment.amount,
            payment_mode=payment.payment_mode,
            payment_info=payment.payment_info,
            other_info=payment.other_info
        )
    db_payment.created_on = datetime.now()
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
        
    return db_payment

@router.get("/payments/FetchAll", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
def read_all_payments(db: Session = Depends(get_db)):
    payments = db.query(Payment).all()
    if not payments:
        raise HTTPException(status_code=404, detail="No payments found")
    return payments


from sqlalchemy import desc

@router.get("/payments/Fetch/{user_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
def read_payment(user_id: int, db: Session = Depends(get_db)):
    user = db.query(LmsUsers).filter(LmsUsers.user_id == user_id).first()
    
    # Check if user exists
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Retrieve the latest payment associated with the user, ordered by creation date in descending order
    latest_payment = db.query(Payment).filter(Payment.user_id == user_id).order_by(desc(Payment.created_on)).first()

    if not latest_payment:
        raise HTTPException(status_code=404, detail="No payments found for this user")

    return latest_payment


@router.put("/payments/verify/{user_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
def verify_payments_and_update_details(
    user_id: int,
    db: Session = Depends(get_db)
):
    # Retrieve the user from the database
    user = db.query(LmsUsers).filter(LmsUsers.user_id == user_id).first()
    
    # Check if user exists
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Retrieve payments associated with the user
    payment_info = db.query(Payment).filter(Payment.user_id == user_id).all()

    # Initialize response dictionary
    response = {
        "user_id": user.user_id,
        "is_payment_done": user.is_payment_done,
        "payments": None  # Default value set to None
    }

    # Add payment details to the response if payments exist
    if payment_info:
        response["payments"] = []
        for payment in  payment_info:
            response["payments"].append({
                "payment_id": payment.payment_id,
                "years": payment.years,
                "amount": payment.amount,
                "created_on": payment.created_on
            })

    # Update the is_payment_done status if all payments are done
    if  payment_info:
        user.is_payment_done = True
        db.add(user)
        db.commit()
        response["is_payment_done"] = True
        response["message"] = "Payments verified. Students can access courses."
    else:
        response["message"] = "No payments found. Students cannot access courses."

    return response

@router.put("/payments/{payment_id}", response_model=None)
def update_payment(
    payment_id: int, 
    payment: PaymentCreate, 
    db: Session = Depends(get_db), 
    current_user: LmsUsers = Depends(get_current_user)
):
    # Check if the payment exists
    db_payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    # Check if the provided course, standard, subject, module, and batch exist in the database
    existing_course = db.query(Course).filter(Course.id == payment.course_id).first()
    existing_standard = db.query(Standard).filter(Standard.id == payment.standard_id).first()
    existing_subject = db.query(Subject).filter(Subject.id == payment.subject_id).first()
    existing_module = db.query(Module).filter(Module.id == payment.module_id).first()
    existing_batch = db.query(Batch).filter(Batch.id == payment.batch_id).first()

    if not all([existing_course, existing_standard, existing_subject, existing_module, existing_batch]):
        raise HTTPException(status_code=404, detail="One or more of course, standard, subject, module, or batch not found")

    # Update the payment
    db_payment.course_id = payment.course_id
    db_payment.standard_id = payment.standard_id
    db_payment.subject_id = payment.subject_id
    db_payment.module_id = payment.module_id
    db_payment.batch_id = payment.batch_id
    db_payment.years = payment.years
    db_payment.amount = payment.amount
    db_payment.payment_mode = payment.payment_mode
    db_payment.payment_info = payment.payment_info
    db_payment.other_info = payment.other_info

    db_payment.updated_on = datetime.now()  
    db.commit()
    db.refresh(db_payment)

    return db_payment


@router.delete("/payments/delete/{payment_id}", response_model=None)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(payment)
    db.commit()
    return {"message": "Payment deleted successfully"}
# @router.get("/payments/", response_model=List[PaymentResponse])
# def read_payments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return db.query(Payment).offset(skip).limit(limit).all()
