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
    offering: Mapped["Offering"] = relationship("Offering", back_populates="timeslot", nullable=True)
    offering_id: Mapped[int] = mapped_column(Integer, ForeignKey("offerings.id"), nullable=True) 
    schedule_id: Mapped[int] = mapped_column(Integer, ForeignKey("schedules.id"), nullable=False)
    schedule: Mapped["Schedule"] = relationship("Schedule", back_populates="timeslots")