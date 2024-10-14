from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship
from db.config import Base

# Booking Model
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    offering_id = Column(Integer, ForeignKey('offerings.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    booked_at = Column(DateTime, nullable=False)

    # Relationships
    offering = relationship("Offering", back_populates="bookings")
    client = relationship("Client", back_populates="bookings")
