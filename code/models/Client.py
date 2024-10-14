from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship
from database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, ForeignKey('users.id'), primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_underage = Column(Boolean, nullable=False)
    guardian_id = Column(String, nullable=True)  # For underage clients

    # Relationships
    user = relationship("User", back_populates="client")
    bookings = relationship("Booking", back_populates="client")