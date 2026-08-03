from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, blockchain
from ..database import get_db

router = APIRouter(prefix="/nurses", tags=["nurses"])


@router.get("/{nurse_id}/verification")
def verify_nurse(nurse_id: int, db: Session = Depends(get_db)):
    nurse = db.query(models.User).filter(
        models.User.id == nurse_id, models.User.role == models.UserRole.caregiver
    ).first()
    if not nurse:
        raise HTTPException(status_code=404, detail="Nurse not found")
    if not nurse.wallet_address:
        raise HTTPException(status_code=400, detail="No wallet address on file for this nurse")

    is_valid = blockchain.is_nurse_license_valid(nurse.wallet_address)
    details = blockchain.get_license_details(nurse.wallet_address) if is_valid else None

    return {"nurse_id": nurse_id, "license_valid": is_valid, "license_details": details}


@router.post("/availability", response_model=schemas.AvailabilityOut)
def add_availability(slot: schemas.AvailabilityCreate, db: Session = Depends(get_db)):
    availability = models.Availability(**slot.model_dump())
    db.add(availability)
    db.commit()
    db.refresh(availability)
    return availability


@router.get("/availability/open")
def list_open_availability(db: Session = Depends(get_db)):
    return db.query(models.Availability).filter(models.Availability.is_booked == 0).all()
