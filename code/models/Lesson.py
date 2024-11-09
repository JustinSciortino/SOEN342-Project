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
    timeslot: Mapped["Timeslot"] = relationship(back_populates="offering", cascade="all, delete-orphan")
    location: Mapped["Location"] = relationship("Location", back_populates="offerings")
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey('locations.id'), nullable=True)
    capacity: Mapped[int] = mapped_column(Integer, nullable=True)
    offerings = relationship("Offering", back_populates="lesson")
    location = relationship("Location", back_populates="lessons")
    location_id = mapped_column(Integer, ForeignKey('locations.id'), nullable=False)
    timeslot = relationship("Timeslot", back_populates="lesson", cascade="all, delete-orphan")

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
    
    def get_specialization(self):
        return self.specialization
    
    def get_type(self):
        return self.type
    
    def get_timeslot(self):
        return self.timeslot
    
