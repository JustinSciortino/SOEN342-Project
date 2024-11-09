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
        return self.offerings
    
    def repr_admin(self):
        return f"\n\tLesson {self.id} is a {self.get_type().name} class with a capacity of {self.get_capacity()} at {self.get_location().get_name()}, {self.get_location().get_city()} on {self.get_timeslot().get_day_of_week()} from {self.get_timeslot().get_start_time()} {self.get_timeslot().get_start_date()} to {self.get_timeslot().get_end_time()} {self.get_timeslot().get_end_date()} doing {self.get_specialization().name}"

    def repr_instructor(self):
        return f"\nLesson ID: {self.get_id()}\nType: {self.get_type().name}\nSpecialization: {self.get_specialization().name}\nLocation: {self.get_location().get_name()}, {self.get_location().get_city()}\nTimeslot: {self.get_timeslot().get_day_of_week()}, {self.get_timeslot().get_start_time()} {self.get_timeslot().get_start_date()} - {self.get_timeslot().get_end_time()} {self.get_timeslot().get_end_date()}\nCapacity: {self.get_capacity()}"