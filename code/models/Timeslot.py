from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
from datetime import datetime

class Timeslot(Base):
    __tablename__ = "timeslots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    day_of_week: Mapped[str] = mapped_column(String, nullable=False)
    start_time: Mapped[Time] = mapped_column(Time, nullable=False)
    start_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[Time] = mapped_column(Time, nullable=False)
    end_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    lesson: Mapped["Lesson"] = relationship(back_populates="timeslot")
    lesson_id: Mapped[int] = mapped_column(Integer, ForeignKey("lessons.id"), nullable=True) 
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
        return f"Timeslot {self.id} is on {self.day_of_week} from {self.start_time} to {self.end_time} starting on {self.start_date} and ending on {self.end_date} for Lesson {self.lesson_id}"

    @classmethod
    def is_conflicting(self, booked_timeslots: list["Timeslot"]):
        new_start_datetime = datetime.combine(self.start_date, self.start_time)
        new_end_datetime = datetime.combine(self.end_date, self.end_time)

        for booked_timeslot in booked_timeslots:
            booked_start_datetime = datetime.combine(booked_timeslot.start_date, booked_timeslot.start_time)
            booked_end_datetime = datetime.combine(booked_timeslot.end_date, booked_timeslot.end_time)

            if booked_start_datetime <= new_end_datetime and new_start_datetime <= booked_end_datetime:
                if booked_timeslot.day_of_week == self.day_of_week:
                    if (booked_timeslot.start_time <= self.start_time < booked_timeslot.end_time) or \
                        (booked_timeslot.start_time < self.end_time <= booked_timeslot.end_time) or \
                        (self.start_time <= booked_timeslot.start_time and booked_timeslot.end_time <= self.end_time):
                        return True
        return False
    
    def get_id(self) -> int:   
        return self.id
    def get_start_time(self):
        return self.start_time
    def get_start_date(self):
        return self.start_date
    def get_end_time(self):
        return self.end_time
    def get_end_date(self):
        return self.end_date
    def get_day_of_week(self) -> str:
        return self.day_of_week
    
