from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base


class Timeslot(Base):
    __tablename__ = "timeslots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    day_of_week: Mapped[str] = mapped_column(String, nullable=False)
    start_time: Mapped[Time] = mapped_column(Time, nullable=False)
    start_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[Time] = mapped_column(Time, nullable=False)
    end_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    offering: Mapped["Offering"] = relationship(back_populates="timeslot")
    offering_id: Mapped[int] = mapped_column(Integer, ForeignKey("offerings.id"), nullable=True) 
    schedule_id: Mapped[int] = mapped_column(Integer, ForeignKey("schedules.id"), nullable=False)
    schedule: Mapped["Schedule"] = relationship("Schedule", back_populates="timeslots")

    def __init__(self, day_of_week: str, start_time: Time, start_date: DateTime, end_time: Time, end_date: DateTime, schedule_id: int):
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.start_date = start_date
        self.end_time = end_time
        self.end_date = end_date
        self.schedule_id = schedule_id
    
    def __repr__(self):
        return f"Timeslot {self.id} is on {self.day_of_week} from {self.start_time} to {self.end_time} starting on {self.start_date} and ending on {self.end_date}"