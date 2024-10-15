from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
from models import Timeslot

class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    timeslots: Mapped[list["Timeslot"]] = relationship("Timeslot", back_populates="schedule", cascade="all, delete-orphan")
    location: Mapped["Location"] = relationship("Location", back_populates="schedule", )
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey("locations.id"), nullable=False)

    def __init__(self, location, location_id:int):
        self.timeslots = []
        self.location = location
        self.location_id = location_id

    def __repr__(self):
        return f"Schedule {self.id} for {self.location} has {len(self.timeslots)} timeslots"
    
    def add_timeslot(self, timeslot: Timeslot):
        self.timeslots.append(timeslot)
        return self
    
    def remove_timeslot(self, timeslot: Timeslot):
        self.timeslots.remove(timeslot)
        return self
    
    def get_timeslots(self):
        return self.timeslots
    
    def get_id(self) -> int:
        return self.id
    
    def delete(self):
        self.timeslots = []
    
    def is_conflicting(self, timeslot: Timeslot):
        from datetime import datetime
        for ts in self.timeslots:
            # Combine date and time to create datetime objects
            ts_start_datetime = datetime.combine(ts.start_date, ts.start_time)
            ts_end_datetime = datetime.combine(ts.end_date, ts.end_time)
            timeslot_start_datetime = datetime.combine(timeslot.start_date, timeslot.start_time)
            timeslot_end_datetime = datetime.combine(timeslot.end_date, timeslot.end_time)
            
            # Check for date range conflicts
            if ts_start_datetime <= timeslot_end_datetime and timeslot_start_datetime <= ts_end_datetime:
                if ts.day_of_week == timeslot.day_of_week:
                    if (ts.start_time <= timeslot.start_time < ts.end_time) or \
                    (ts.start_time < timeslot.end_time <= ts.end_time) or \
                    (timeslot.start_time <= ts.start_time and ts.end_time <= timeslot.end_time):
                        return True
        return False