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
    lesson = relationship("Lesson", back_populates="offering")
    instructor_id : Mapped[int] = mapped_column(Integer, ForeignKey('instructors.id'), nullable=False)
    instructor: Mapped["Instructor"] = relationship("Instructor", back_populates="offerings")
    status: Mapped[str] = mapped_column(String, default="Available")  
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="offering", cascade="all, delete")
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
            return(
                f"\nOffering ID: {self.get_id()}\n"
                f"Location: {lesson.get_location().get_name()}, {lesson.get_location().get_address()} {lesson.get_location().get_city()}\n"
                f"Capacity: {lesson.get_capacity()}\n"
                f"Number of bookings: {len(self.bookings)}\n"
                f"Timeslot: {lesson.get_timeslot().get_day_of_week()}, {lesson.get_timeslot().get_start_time()} - {lesson.get_timeslot().get_end_time()}\n"
                f"Available from {lesson.get_timeslot().get_start_date()} to {lesson.get_timeslot().get_end_date()}\n"
                f"Offering Type: {lesson.get_type().value}\n"
                f"Specialization: {lesson.get_specialization().value}\n"
                f"Instructor: {self.instructor.get_name()}\n"
                f"Status: {self.get_status()}"
            )
            
        else:
            return (
                f"\nOffering ID: {self.get_id()}\n"
                f"Location: {lesson.get_location().get_name()}, {lesson.get_location().get_address()} {lesson.get_location().get_city()}\n"
                f"Capacity: Private Lesson\n"
                f"Timeslot: {lesson.get_timeslot().get_day_of_week()}, {lesson.get_timeslot().get_start_time()} - {lesson.get_timeslot().get_end_time()}\n"
                f"Available from {lesson.get_timeslot().get_start_date()} to {lesson.get_timeslot().get_end_date()}\n"
                f"Offering Type: {lesson.get_type().value}\n"
                f"Specialization: {lesson.get_specialization().value}\n"
                f"Instructor: {self.instructor.get_name()}\n"
                f"Status: {self.get_status()}"
            )
            
    def repr_instructor(self):
        lesson = self.get_lesson()
        capacity_info = (
            f"Capacity: {lesson.get_capacity()}\n"
            if lesson.get_type().value != 'private'
            else "Capacity: Private Lesson\n"
        )
        return (
            f"\nOffering ID: {self.get_id()}\n"
            f"Location ID: {lesson.get_location().get_id()}\n"
            f"Location: {lesson.get_location().name}, {lesson.get_location().get_city()}\n"
            f"{capacity_info}"
            f"Timeslot: {lesson.get_timeslot().get_day_of_week()}, {lesson.get_timeslot().get_start_time()} - {lesson.get_timeslot().get_end_time()}\n"
            f"Available from {lesson.get_timeslot().get_start_date()} to {lesson.get_timeslot().get_end_date()}"
            f"Offering Type: {lesson.get_type().value}\n"
        )
    
    def repr_client(self):
        lesson = self.get_lesson()
        capacity_info = (
            f"Capacity: {lesson.get_capacity()}\n"
            if lesson.get_type().value != 'private' 
            else "Capacity: Private Lesson\n"
        )
        return (
            f"\nOffering ID: {self.get_id()}\n"
            f"Location: {lesson.get_location().get_name()}, {lesson.get_location().get_city()}\n"
            f"{capacity_info}"
            f"Timeslot: {lesson.get_timeslot().get_day_of_week()}, {lesson.get_timeslot().get_start_time()} - {lesson.get_timeslot().get_end_time()}\n"
            f"Offering Type: {lesson.get_type().value}\n"
            f"Available from {lesson.get_timeslot().get_start_date()} to {lesson.get_timeslot().get_end_date()}\n"
            f"Specialization: {lesson.get_specialization().value}\n"
            f"Instructor: {self.instructor.get_name()}\n"
            f"Status: {self.get_status()}"  
        )
    
    def repr_client_booked(self):
        lesson = self.get_lesson()
        capacity_info = (
            f"Capacity: {lesson.get_capacity()}\n"
            if lesson.get_type().value != 'private'
            else "Capacity: Private Lesson\n"
        )
        return (
            f"\nOffering ID: {self.get_id()}\n"
            f"Location: {lesson.get_location().get_name()}, {lesson.get_location().get_city()}\n"
            f"{capacity_info}"
            f"Timeslot: {lesson.get_timeslot().get_day_of_week()}, {lesson.get_timeslot().get_start_time()} - {lesson.get_timeslot().get_end_time()}\n"
            f"Offering Type: {lesson.get_type().value}\n"
            f"Available from {lesson.get_timeslot().get_start_date()} to {lesson.get_timeslot().get_end_date()}\n"
            f"Specialization: {lesson.get_specialization().value}\n"
            f"Instructor: {self.instructor.get_name()}\n"
            f"Status: Non-Availble"  
        )

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
    
    def get_lesson(self):
        return self.lesson
    