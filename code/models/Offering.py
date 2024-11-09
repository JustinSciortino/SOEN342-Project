from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
from .LessonType import LessonType
from .SpecializationType import SpecializationType
from .Timeslot import Timeslot
from .Lesson import Lesson



class Offering(Base):
    __tablename__ = "offerings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    lesson_id: Mapped[int]=mapped_column(Integer, ForeignKey('lessons.id'), nullable=False)
    lesson = relationship("Lesson", back_populates="offerings")
    instructor_id : Mapped[int] = mapped_column(Integer, ForeignKey('instructors.id'), nullable=False)
    instructor: Mapped["Instructor"] = relationship("Instructor", back_populates="offerings")
    status: Mapped[str] = mapped_column(String, default="Not-Available")  #? Only made not available to the client if they already booked the offering
    #! Status needs to be refactored
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="offering")
    is_cancelled: Mapped[bool] = mapped_column(Boolean, default=False)

    def __init__(self, instructor: "Instructor", lesson: "Lesson"):
        self.is_cancelled = False
        self.instructor = instructor
        self.instructor_id = instructor.get_id()
        self.lesson = lesson
        self.lesson_id = lesson.get_id()
        self.status = "Not-Available"
        self.bookings = []

    def repr_user(self):
        return f"\nOffering {self.id} is a {self.type.name} class with a capacity of {self.capacity} and {self.capacity-len(self.bookings)} spots available at {self.location}"
    
    def repr_admin(self):
        if self.type == LessonType.group:
            return f"\nOffering {self.id} is a {self.type.name} class with a capacity of {self.capacity} and the course is {self.specialization.name}, {len(self.bookings)} number of bookings and {self.capacity-len(self.bookings)} spots available at {self.location} and is {self.status}"
        else:
            return f"\nOffering {self.id} is a {self.type.name} class and the course is {self.specialization.name}, at {self.location} and is {self.status}"
          
    def repr_instructor(self):
        return (
            f"Offering ID: {self.id}\n"
            f"Location: {self.location.name}, {self.location.city}\n"
            f"Capacity: {self.capacity}\n"
            f"Timeslot: {self.timeslot.day_of_week}, {self.timeslot.start_time} - {self.timeslot.end_time}\n"
            f"Offering Type: {self.type.value}\n"
            f"Available from {self.timeslot.start_date} to {self.timeslot.end_date}"
        )
    
    def repr_client(self):
        return (
            f"Offering ID: {self.id}\n"
            f"Location: {self.location.name}, {self.location.city}\n"
            f"Capacity: {self.capacity}\n"
            f"Timeslot: {self.timeslot.day_of_week}, {self.timeslot.start_time} - {self.timeslot.end_time}\n"
            f"Offering Type: {self.type.value}\n"
            f"Available from {self.timeslot.start_date} to {self.timeslot.end_date}\n"
            f"Specialization: {self.specialization.value}\n"
            f"Instructor: {self.instructor.name}\n"
            f"Status: {self.status}"  
        )

    def update_status(self, client : "Client"):
        client_has_booked = any(booking.client_id == client.get_id() for booking in self.bookings)
        
        no_spots_left = self.capacity - len(self.bookings) == 0

        booked_timeslots = [booking.offering.timeslot for booking in client.get_bookings()]

        time_conflict = Timeslot.is_conflicting(self.timeslot, booked_timeslots)

        if client_has_booked:
            self.status = "Not Available (Already Booked)"
        elif no_spots_left:
            self.status = "Not Available (No Spots Left)"
        elif time_conflict:
            self.status = "Not Available (Time Conflict)"
        

    def get_id(self) -> int:
        return self.id
    
    def get_type(self) -> LessonType:
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
    