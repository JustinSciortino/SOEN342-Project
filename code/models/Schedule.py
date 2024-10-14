from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base

class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    timeslots: Mapped[list["Timeslot"]] = relationship("Timeslot", back_populates="schedule")
    location: Mapped["Location"] = relationship("Location", back_populates="schedule")
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey("locations.id"), nullable=False)

    def __init__(self):
        self.timeslots = []