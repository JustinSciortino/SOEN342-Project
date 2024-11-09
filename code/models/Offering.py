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
    status: Mapped[str] = mapped_column(String, default="Available")  #? Only made not available to the client if they already booked the offering
    #! Status needs to be refactored
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="offering")
    is_cancelled: Mapped[bool] = mapped_column(Boolean, default=False)

    def __init__(self, instructor: "Instructor", lesson: "Lesson"):
        self.is_cancelled = False
        self.instructor = instructor
        self.instructor_id = instructor.get_id()
        self.lesson = lesson
        self.lesson_id = lesson.get_id()
        self.status = "Available"
        self.bookings = []

    def repr_user(self):
        lesson = self.get_lesson()
        return f"\n\tOffering {self.get_id()} is a {lesson.get_type().name} class with a capacity of {lesson.get_capacity()} and {lesson.get_capacity()-len(self.bookings)} spots available at {lesson.get_location().offering_repr()}"
    
    def repr_admin(self):
        lesson = self.get_lesson()
        if lesson.get_type() == LessonType.group:
            return f"\n\tOffering {self.get_id()} is a {lesson.get_type().name} class with a capacity of {lesson.get_capacity()} and the course is {lesson.get_specialization().name}, {len(self.bookings)} number of bookings and {lesson.get_capacity()-len(self.bookings)} spots available at {lesson.get_location().offering_repr()} and is {self.get_status()}"
        else:
            return f"\n\tOffering {self.get_id()} is a {lesson.get_type().name} class and the course is {lesson.get_specialization().name}, at {lesson.get_location().offering_repr()} and is {self.get_status()}"
          
    def repr_instructor(self):
        lesson = self.get_lesson()
        return (
            f"\nOffering ID: {self.get_id()}\n"
            f"Location ID: {lesson.get_location().get_id()}\n"
            f"Location: {lesson.get_location().name}, {lesson.get_location().get_city()}\n"
            f"Capacity: {lesson.get_capacity()}\n"
            f"Timeslot: {lesson.get_timeslot().get_day_of_week()}, {lesson.get_timeslot().get_start_time()} - {lesson.get_timeslot().get_end_time()}\n"
            f"Available from {lesson.get_timeslot().get_start_date()} to {lesson.get_timeslot().get_end_date()}"
            f"Offering Type: {lesson.get_type().value}\n"
        )
    
    def repr_client(self):
        lesson = self.get_lesson()
        return (
            f"\nOffering ID: {self.get_id()}\n"
            f"Location: {lesson.get_location().get_name()}, {lesson.get_location().get_city()}\n"
            f"Capacity: {lesson.get_capacity()}\n"
            f"Timeslot: {lesson.get_timeslot().get_day_of_week()}, {lesson.get_timeslot().get_start_time()} - {lesson.get_timeslot().get_end_time()}\n"
            f"Offering Type: {lesson.get_type().value}\n"
            f"Available from {lesson.get_timeslot().get_start_date()} to {lesson.get_timeslot().get_end_date()}\n"
            f"Specialization: {lesson.get_specialization().value}\n"
            f"Instructor: {self.instructor.get_name()}\n"
            f"Status: {self.get_status()}"  
        )

    def update_status(self, client : "Client"):
        client_has_booked = any(booking.get_client_id() == client.get_id() for booking in self.bookings)
        
        no_spots_left = self.get_lesson().get_capacity() - len(self.bookings) == 0

        booked_timeslots = [booking.get_offering().get_lesson().get_timeslot() for booking in client.get_bookings()]

        time_conflict = Timeslot.is_conflicting(self.get_lesson().get_timeslot(), booked_timeslots)

        if client_has_booked:
            self.set_status("Not Available (Already Booked)")

        elif no_spots_left:
            self.set_status("Not Available (No Spots Left)")

        elif time_conflict:
            self.set_status("Not Available (Time Conflict)")
        

    def get_id(self) -> int:
        return self.id

    def get_instructor(self):
        return self.instructor
    
    def get_status(self) -> str:
        return self.status
    
    def set_status(self, status: str):
        self.status = status
    
    def get_bookings(self):
        return self.bookings
    
    def get_is_cancelled(self) -> bool:
        return self.is_cancelled
    
    def set_is_cancelled(self, is_cancelled: bool):
        self.is_cancelled = is_cancelled
    
    
    def cancel(self):
        self.is_cancelled = True
        self.get_lesson().set_location(None)
        self.set_status("Not-Available") 
        for booking in self.bookings:
            booking.cancel()

    def cancel_offering(self):
        self.set_status("Not-Available") 
        self.set_is_cancelled(True)
        for booking in self.bookings:
            booking.cancel()
    
    
    def add_booking(self, booking: "Booking"):
        if self.get_status() == "Not-Available":
            raise ValueError("Offering is not available for booking")
        self.bookings.append(booking)
        return self
    
    def get_lesson(self):
        return self.lesson
    