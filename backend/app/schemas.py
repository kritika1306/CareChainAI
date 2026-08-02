from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from .models import UserRole, BookingStatus


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: UserRole
    wallet_address: Optional[str] = None


class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: UserRole
    wallet_address: Optional[str] = None

    class Config:
        from_attributes = True


class AvailabilityCreate(BaseModel):
    caregiver_id: int
    start_time: datetime
    end_time: datetime


class AvailabilityOut(BaseModel):
    id: int
    caregiver_id: int
    start_time: datetime
    end_time: datetime
    is_booked: int

    class Config:
        from_attributes = True


class BookingCreate(BaseModel):
    patient_id: int
    caregiver_id: int
    availability_id: int


class BookingOut(BaseModel):
    id: int
    patient_id: int
    caregiver_id: int
    status: BookingStatus
    created_at: datetime

    class Config:
        from_attributes = True


class PaymentCreate(BaseModel):
    booking_id: int
    amount: float
