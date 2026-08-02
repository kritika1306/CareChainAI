from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base


class UserRole(str, enum.Enum):
    patient = "patient"
    caregiver = "caregiver"
    admin = "admin"


class BookingStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    wallet_address = Column(String, nullable=True)  # for caregivers, links to on-chain license
    created_at = Column(DateTime, default=datetime.utcnow)

    bookings_as_patient = relationship(
        "Booking", back_populates="patient", foreign_keys="Booking.patient_id"
    )
    bookings_as_caregiver = relationship(
        "Booking", back_populates="caregiver", foreign_keys="Booking.caregiver_id"
    )
    availability_slots = relationship("Availability", back_populates="caregiver")


class Availability(Base):
    __tablename__ = "availability"

    id = Column(Integer, primary_key=True, index=True)
    caregiver_id = Column(Integer, ForeignKey("users.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_booked = Column(Integer, default=0)  # 0 = open, 1 = booked

    caregiver = relationship("User", back_populates="availability_slots")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    caregiver_id = Column(Integer, ForeignKey("users.id"))
    availability_id = Column(Integer, ForeignKey("availability.id"))
    status = Column(Enum(BookingStatus), default=BookingStatus.pending)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("User", back_populates="bookings_as_patient", foreign_keys=[patient_id])
    caregiver = relationship("User", back_populates="bookings_as_caregiver", foreign_keys=[caregiver_id])
    payment = relationship("Payment", back_populates="booking", uselist=False)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), unique=True)
    amount = Column(Float, nullable=False)
    status = Column(String, default="pending")  # pending, paid, refunded
    created_at = Column(DateTime, default=datetime.utcnow)

    booking = relationship("Booking", back_populates="payment")
