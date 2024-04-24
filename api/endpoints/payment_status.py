import hashlib
import hmac
import json

from fastapi import APIRouter, Depends, HTTPException, Header, Request
import stripe
from decouple import config
import os
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from db.session import get_db
from ..models import PaymentStatus

router = APIRouter()

stripe.api_key = config("STRIPE_API_KEY")
# stripe_webhook_secret = config("STRIPE_WEBHOOK_SECRET")
stripe_webhook_secret = "whsec_cc6d3c8d1f3cc04df875da343ff7523316b7859310d92fb65dd5956c04981fae"

# print(stripe_webhook_secret)
# @router.post("/create-payment-intent")
# async def create_payment_intent(amount: int, currency: str = "inr"):
#     try:
#         payment_intent = stripe.PaymentIntent.create(
#             amount=amount,
#             currency=currency,
#             payment_method_types=["card"],
#         )
#         return {"clientSecret": payment_intent.client_secret}
#     except Exception as e:
#         return {"error": str(e)}
#
# @router.post("/webhook")
# async def stripe_webhook(request: Request):
#     payload = await request.body()
#     sig_header = request.headers.get('Stripe-Signature')
#     print("Request body:", payload.decode())  # Decode bytes to string
#     print("Stripe-Signature header:", sig_header)
#
#     try:
#         # Verify webhook signature
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, stripe_webhook_secret
#         )
#     except ValueError as e:
#         # Invalid payload
#         raise HTTPException(status_code=400, detail="Invalid payload")
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         raise HTTPException(status_code=400, detail="Invalid signature")
#
#     # Handle specific webhook event types
#     if event['type'] == 'payment_intent.succeeded':
#         payment_intent = event['data']['object']
#         # Update payment status in your database
#         # Notify user about successful payment, etc.
#
#     elif event['type'] == 'payment_intent.payment_failed':
#         payment_intent = event['data']['object']
#         # Handle failed payment scenario
#         # Notify user about payment failure, etc.
#
#     # Return a 200 OK response to acknowledge receipt of the event
#     return {"received": True}

# if stripe_webhook_secret is None:
#     raise EnvironmentError("Stripe webhook secret is not set.")


@router.post("/process_payment/")
async def process_payment(amount: int):
    try:
        # Create a charge using the Stripe API
        charge = stripe.Charge.create(
            amount=amount,
            source="tok_visa",
            description="Payment for Demo"
        )
        return {"status": "success", "charge_id": charge.id}

    except stripe.error.CardError as e:
        return {"status": "error", "message": str(e)}
    except stripe.error.StripeError as e:
        return {"status": "error", "message": "Something went wrong. Please try again later."}

# @router.post("/process_payment/")
# async def process_payment(amount: int, token: str = Header(None), username: str = Depends(verify_token)):
#     try:
#         # Verify token and extract username
#         if not username:
#             raise HTTPException(status_code=401, detail="Invalid or missing token")
#
#         # Create a charge using the Stripe API
#         charge = stripe.Charge.create(
#             amount=amount,
#             currency="usd",  # Change currency if necessary
#             source=token,
#             description="Payment for Demo"
#         )
#         return {"status": "success", "charge_id": charge.id}
#
#     except stripe.error.CardError as e:
#         return {"status": "error", "message": str(e)}
#     except stripe.error.StripeError as e:
#         return {"status": "error", "message": "Something went wrong. Please try again later."}



# def create_checkout_session(db: Session, price: int, metadata: dict):
#     db_session = PaymentStatus(price=price, **metadata)
#     db.add(db_session)
#     db.commit()
#     db.refresh(db_session)
#     return db_session
#
# def get_checkout_session(db: Session, session_id: int):
#     return db.query(PaymentStatus).filter(PaymentStatus.id == session_id).first()
#
# def update_checkout_session(db: Session, session_id: int, new_price: int):
#     db_session = db.query(PaymentStatus).filter(PaymentStatus.id == session_id).first()
#     db_session.price = new_price
#     db.commit()
#     db.refresh(db_session)
#     return db_session
#
# def delete_checkout_session(db: Session, session_id: int):
#     db_session = db.query(PaymentStatus).filter(PaymentStatus.id == session_id).first()
#     db.delete(db_session)
#     db.commit()


# @router.get("/checkout/")
# async def create_checkout_session(price: int, db: Session = Depends(get_db)):
#     try:
#         # Create a checkout session
#         checkout_session = stripe.checkout.Session.create(
#             line_items=[
#                 {
#                     "price_data": {
#                         "currency": "usd",
#                         "product_data": {
#                             "name": "FastAPI Stripe Checkout",
#                         },
#                         "unit_amount": price * 100,
#                     },
#                     "quantity": 1,
#                 }
#             ],
#             mode="payment",
#             success_url=os.getenv("BASE_URL") + "/success/",
#             cancel_url=os.getenv("BASE_URL") + "/cancel/",
#             customer_email="ping@fastapitutorial.com",
#         )
#
#         # Save session metadata to the database
#         metadata = {
#             "user_id": 3,
#             "email": "abc@gmail.com",
#             "request_id": 1234567890
#         }
#         create_checkout_session(db, price, metadata)
#
#         # Redirect user to checkout session URL
#         return RedirectResponse(checkout_session.url, status_code=303)
#
#     except stripe.error.StripeError as e:
#         # Handle Stripe errors
#         raise HTTPException(status_code=400, detail=str(e))
#
#     except Exception as e:
#         # Handle other errors
#         raise HTTPException(status_code=500, detail=str(e))



