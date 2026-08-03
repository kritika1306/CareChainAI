from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/")
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == payment.booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    db_payment = models.Payment(
        booking_id=payment.booking_id, amount=payment.amount, status="paid"
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


@router.get("/booking/{booking_id}")
def get_payment_for_booking(booking_id: int, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.booking_id == booking_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="No payment found for this booking")
    return payment
