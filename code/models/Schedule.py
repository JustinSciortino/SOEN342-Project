from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
from models import Timeslot

class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    timeslots: Mapped[list["Timeslot"]] = relationship("Timeslot", back_populates="schedule")
    location: Mapped["Location"] = relationship("Location", back_populates="schedule")
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
    
    def is_conflicting(self, timeslot: Timeslot): #TODO: Also needs to check start and end date for conflicts
        for ts in self.timeslots:
            if ts.day_of_week == timeslot.day_of_week:
                if ts.start_time <= timeslot.start_time <= ts.end_time:
                    return True
                if ts.start_time <= timeslot.end_time <= ts.end_time:
                    return True
        return False