from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship
from db.config import Base
from OfferingType import OfferingType

# Offering Model
class Offering(Base):
    __tablename__ = "offerings"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(OfferingType), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    schedule_id = Column(Integer, ForeignKey('schedules.id'), nullable=False)
    instructor_id = Column(Integer, ForeignKey('instructors.id'), nullable=True)
    is_available = Column(Boolean, default=True)
    status = Column(String, default="Available")  # Adding status field to track offering state

    # Relationships
    schedule = relationship("Schedule", back_populates="offerings")
    instructor = relationship("Instructor", back_populates="offerings")
    bookings = relationship("Booking", back_populates="offering")