from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
from OfferingType import OfferingType

# Offering Model
class Offering(Base):
    __tablename__ = "offerings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(Enum(OfferingType), nullable=False)
    instructor_id : Mapped[int] = mapped_column(Integer, ForeignKey('instructors.id'), nullable=True)
    instructor: Mapped["Instructor"] = relationship("Instructor", back_populates="offerings")
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[str] = mapped_column(String, default="Not-Available")  
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="offering", nullable=True)
    bookings_id: Mapped[list[int]]=mapped_column(Mapped[list[int]], default=[])
    timeslot: Mapped["Timeslot"] = relationship("Timeslot", back_populates="offerings", nullable=False)
    timeslot_id: Mapped[int] = mapped_column(Integer, ForeignKey('timeslots.id'), nullable=False)
    location: Mapped["Location"] = relationship("Location", back_populates="offerings", nullable=False)
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey('locations.id'), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)

    def __init__(self):
        self.bookings = []


    #start_time = Column(Time, nullable=False)
    #end_time = Column(Time, nullable=False)