from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
from models import Minor    

class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True, autoincrement=True)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    is_legal_guardian: Mapped[bool] = mapped_column(Boolean, nullable=False)
    minor: Mapped["Minor"] = relationship("Minor", back_populates="guardian")  # For underage clients
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="client", cascade="all, delete-orphan")

    __mapper_args__ = {
        "polymorphic_identity": "client",
    }

    def __init__(self, phone_number: str, is_legal_guardian: bool, minor_name: str = None, minor_age: int = None):
        self.phone_number = phone_number
        self.is_legal_guardian = is_legal_guardian
        if is_legal_guardian:
            self.minor = Minor(self, minor_name, minor_age)
        else:
            self.minor = None
        self.bookings = []

    def __repr__(self) -> str:
        if self.is_legal_guardian:
            return f"Client {self.id} ({self.phone_number}) is a legal guardian of {self.minor}"
        return f"Client {self.id} ({self.phone_number}) is a client"
    
    def cancel_booking(self, booking: Booking):
        if booking in self.bookings:
            booking.cancel()  # Cancel the booking
            self.bookings.remove(booking)  # Remove from client's bookings

    def delete(self):
        # Cancel all associated bookings before deletion
        for booking in self.bookings:
            booking.cancel()
        self.bookings = []  
    
    def get_id(self) -> int:
        return self.id
    
    def get_phone_number(self) -> str:
        return self.phone_number
    
    def is_legal_guardian(self) -> bool:
        return self.is_legal_guardian
    
    def get_minor(self) -> Minor:  
        return self.minor
    
    def get_bookings(self) -> list["Booking"]:
        return self.bookings