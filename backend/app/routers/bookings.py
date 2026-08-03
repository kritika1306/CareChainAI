from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, blockchain
from ..database import get_db

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("/", response_model=schemas.BookingOut)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    slot = db.query(models.Availability).filter(
        models.Availability.id == booking.availability_id, models.Availability.is_booked == 0
    ).first()
    if not slot:
        raise HTTPException(status_code=400, detail="Availability slot is not open")

    caregiver = db.query(models.User).filter(models.User.id == booking.caregiver_id).first()
    if not caregiver:
        raise HTTPException(status_code=404, detail="Caregiver not found")

    # Enforce license verification before allowing a booking to be confirmed.
    if caregiver.wallet_address:
        if not blockchain.is_nurse_license_valid(caregiver.wallet_address):
            raise HTTPException(
                status_code=403,
                detail="This caregiver's license is not currently valid on-chain",
            )

    db_booking = models.Booking(
        patient_id=booking.patient_id,
        caregiver_id=booking.caregiver_id,
        availability_id=booking.availability_id,
        status=models.BookingStatus.confirmed,
    )
    slot.is_booked = 1

    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


@router.get("/patient/{patient_id}")
def get_patient_bookings(patient_id: int, db: Session = Depends(get_db)):
    return db.query(models.Booking).filter(models.Booking.patient_id == patient_id).all()


@router.patch("/{booking_id}/cancel")
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking.status = models.BookingStatus.cancelled
    db.commit()
    return {"status": "cancelled"}
