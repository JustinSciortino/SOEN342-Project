from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.config import Base
from .LessonType import LessonType
from .SpecializationType import SpecializationType
from .Timeslot import Timeslot

class Lesson(Base):
    __tablename__ = 'lessons'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = mapped_column(Enum(LessonType), nullable=False)
    specialization = mapped_column(Enum(SpecializationType), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=True)
    offering = relationship("Offering", back_populates="lesson", cascade="all, delete-orphan", uselist=False)
    location = relationship("Location", back_populates="lessons")
    location_id = mapped_column(Integer, ForeignKey('locations.id'), nullable=False)
    timeslot = relationship("Timeslot", back_populates="lesson", cascade="all, delete-orphan", uselist=False)

    def __init__(self, type: LessonType, specialization: SpecializationType, location: "Location", timeslot: "Timeslot", capacity: int = None):    
        self.type = type
        self.specialization = specialization
        self.location = location
        self.location_id = location.get_id()
        self.timeslot = timeslot
        self.capacity = capacity

    def get_capacity(self):
        return self.capacity
    
    def get_id(self):
        return self.id
    
    def get_location(self):
        return self.location
    
    def get_location_id(self):
        return self.location_id
    
    def set_location(self, location):
        self.location = location
        if not location:
            self.location_id = location.get_id
        else:
            self.location_id = None
    
    def get_specialization(self):
        return self.specialization
    
    def get_type(self):
        return self.type
    
    def get_timeslot(self):
        return self.timeslot
    
    def get_offerings(self):
        return self.offering
    
    def repr_admin(self):
        if self.get_type() == LessonType.group:
            return(
                f"\nLesson ID: {self.id}\n"
                f"Location: {self.get_location().get_name()}, {self.get_location().get_address()} {self.get_location().get_city()}\n"
                f"Capacity: {self.get_capacity()}\n"
                f"Timeslot: {self.get_timeslot().get_day_of_week()}, {self.get_timeslot().get_start_time()} - {self.get_timeslot().get_end_time()}\n"
                f"Available from {self.get_timeslot().get_start_date()} to {self.get_timeslot().get_end_date()}\n"
                f"Lesson Type: {self.get_type().value}\n"
                f"Specialization: {self.get_specialization().value}\n"
                f"Offering ID: {self.get_offerings().get_id() if self.get_offerings() is not None else 'None'}\n"
            )
        else:
            return(
                f"\nLesson ID: {self.id}\n"
                f"Location: {self.get_location().get_name()}, {self.get_location().get_address()} {self.get_location().get_city()}\n"
                f"Capacity: Private Lesson\n"
                f"Timeslot: {self.get_timeslot().get_day_of_week()}, {self.get_timeslot().get_start_time()} - {self.get_timeslot().get_end_time()}\n"
                f"Available from {self.get_timeslot().get_start_date()} to {self.get_timeslot().get_end_date()}\n"
                f"Lesson Type: {self.get_type().value}\n"
                f"Specialization: {self.get_specialization().value}\n"
                f"Offering ID: {self.get_offerings().get_id() if self.get_offerings() is not None else 'None'}\n"
            )

    def repr_instructor(self):
        if self.get_type() == LessonType.group:
            return(
                f"\nLesson ID: {self.id}\n"
                f"Location: {self.get_location().get_name()}, {self.get_location().get_city()}\n"
                f"Capacity: {self.get_capacity()}\n"
                f"Timeslot: {self.get_timeslot().get_day_of_week()}, {self.get_timeslot().get_start_time()} - {self.get_timeslot().get_end_time()}\n"
                f"Available from {self.get_timeslot().get_start_date()} to {self.get_timeslot().get_end_date()}\n"
                f"Lesson Type: {self.get_type().value}\n"
                f"Specialization: {self.get_specialization().value}"
            )
        else:
            return(
                f"\nLesson ID: {self.id}\n"
                f"Location: {self.get_location().get_name()}, {self.get_location().get_city()}\n"
                f"Capacity: Private Lesson\n"
                f"Timeslot: {self.get_timeslot().get_day_of_week()}, {self.get_timeslot().get_start_time()} - {self.get_timeslot().get_end_time()}\n"
                f"Available from {self.get_timeslot().get_start_date()} to {self.get_timeslot().get_end_date()}\n"
                f"Lesson Type: {self.get_type().value}\n"
                f"Specialization: {self.get_specialization().value}"
            )