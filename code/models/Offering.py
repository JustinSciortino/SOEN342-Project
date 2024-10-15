from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
from .OfferingType import OfferingType

# Offering Model
class Offering(Base):
    __tablename__ = "offerings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    type = mapped_column(Enum(OfferingType), nullable=False)
    instructor_id : Mapped[int] = mapped_column(Integer, ForeignKey('instructors.id'), nullable=True)
    instructor: Mapped["Instructor"] = relationship("Instructor", back_populates="offerings")
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[str] = mapped_column(String, default="Not-Available")  
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="offering")
    #bookings_id: Mapped[list[int]]=mapped_column(ARRAY(Integer), default=[])
    timeslot: Mapped["Timeslot"] = relationship(back_populates="offering")
    #timeslot_id: Mapped[int] = mapped_column(Integer, ForeignKey('timeslots.id'), nullable=False)
    location: Mapped["Location"] = relationship("Location", back_populates="offerings")
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey('locations.id'), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)

    def __init__(self, 
                 offering_type: OfferingType, 
                 instructor_id: int, 
                 is_available: bool, 
                 status: str, 
                 location_id: int, 
                 capacity: int):
        self.type = offering_type
        self.instructor_id = instructor_id
        self.is_available = is_available
        self.status = status
        self.location_id = location_id
        self.capacity = capacity
        self.bookings = []



    #start_time = Column(Time, nullable=False)
    #end_time = Column(Time, nullable=False)