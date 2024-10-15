from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
from .OfferingType import OfferingType
from .SpecializationType import SpecializationType

# Offering Model
class Offering(Base):
    __tablename__ = "offerings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    type = mapped_column(Enum(OfferingType), nullable=False)
    instructor_id : Mapped[int] = mapped_column(Integer, ForeignKey('instructors.id'), nullable=True)
    instructor: Mapped["Instructor"] = relationship("Instructor", back_populates="offerings")
    is_available: Mapped[bool] = mapped_column(Boolean, default=False) #? Only available once instructor is assigned
    status: Mapped[str] = mapped_column(String, default="Not-Available")  #? Only made not available to the client if they already booked the offering
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="offering")
    specialization = mapped_column(Enum(SpecializationType), nullable=False)
    #bookings_id: Mapped[list[int]]=mapped_column(ARRAY(Integer), default=[])
    timeslot: Mapped["Timeslot"] = relationship(back_populates="offering", cascade="all, delete-orphan")
    #timeslot_id: Mapped[int] = mapped_column(Integer, ForeignKey('timeslots.id'), nullable=False)
    location: Mapped["Location"] = relationship("Location", back_populates="offerings")
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey('locations.id'), nullable=True)
    capacity: Mapped[int] = mapped_column(Integer, nullable=True)
    is_cancelled: Mapped[bool] = mapped_column(Boolean, default=False)

    def __init__(self, 
                 offering_type: OfferingType, 
                 specialization: SpecializationType, 
                 location: "Location", 
                 capacity: int, 
                 timeslot: "Timeslot"):
        self.type = offering_type
        self.is_cancelled = False
        self.timeslot = timeslot
        self.specialization = specialization
        self.instructor = None
        self.instructor_id = None
        self.location = location
        self.location_id = location.get_id()
        self.is_available = False
        self.status = "Not-Available"
        self.capacity = capacity
        self.bookings = []

    def repr_user(self):
        return f"\nOffering {self.id} is a {self.type.name} class with a capacity of {self.capacity} and {self.capacity-len(self.bookings)} spots available at {self.location}"
    
    def repr_admin(self):
        if self.type == OfferingType.group:
            return f"\nOffering {self.id} is a {self.type.name} class with a capacity of {self.capacity} and the course is {self.specialization.name}, {len(self.bookings)} number of bookings and {self.capacity-len(self.bookings)} spots available at {self.location} and is {self.status}"
        else:
            return f"\nOffering {self.id} is a {self.type.name} class and the course is {self.specialization.name}, at {self.location} and is {self.status}"


    def get_id(self) -> int:
        return self.id
    
    def get_type(self) -> OfferingType:
        return self.type

    def get_instructor(self):
        return self.instructor
    
    def set_instructor(self, instructor: "Instructor"):
        self.instructor = instructor
        return self
    
    def get_is_available(self) -> bool:
        return self.is_available
    
    def set_is_available(self, is_available: bool):
        self.is_available = is_available
        return self
    
    def get_status(self) -> str:
        return self.status
    
    def set_status(self, status: str):
        self.status = status
        return self
    
    def get_bookings(self):
        return self.bookings
    
    def get_timeslot(self):
        return self.timeslot
    
    def get_location(self):
        return self.location
    
    def get_capacity(self) -> int:
        return self.capacity
    
    def get_specialization(self) -> SpecializationType:
        return self.specialization
    
    def cancel(self):
        self.is_cancelled = True
        self.location= None
        self.location_id = None
        self.status = "Not-Available"
        for booking in self.bookings:
            booking.cancel()

    def cancel_offering(self):
        self.status = "Not-Available"
        self.is_available = False
        self.is_cancelled = True
        for booking in self.bookings:
            booking.cancel()
    
    def set_capacity(self, capacity: int):
        if capacity < len(self.bookings):
            raise ValueError("Capacity cannot be less than the number of bookings")
        self.capacity = capacity
        return self
    
    def add_booking(self, booking: "Booking"):
        if self.status == "Not-Available":
            raise ValueError("Offering is not available for booking")
        self.bookings.append(booking)
        return self
    