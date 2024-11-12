from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.config import Base
from models import Minor

# Booking Model
class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client: Mapped["Client"] = relationship("Client", back_populates="bookings")
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey('clients.id'), nullable=False)
    minor_id: Mapped[int] = mapped_column(Integer, ForeignKey('minors.id'), nullable=True)
    minor: Mapped["Minor"] = relationship("Minor", back_populates="bookings")
    is_cancelled: Mapped[bool] = mapped_column(Boolean, default=False)
    offering_id: Mapped[int] = mapped_column(Integer, ForeignKey('offerings.id'), nullable=False)
    offering: Mapped["Offering"] = relationship("Offering", back_populates="bookings")
    


    def __init__(self, client: "Client", offering: "Offering", minor:"Minor"=None):
        self.client = client
        self.is_cancelled = False
        self.offering = offering
        self.offering_id = offering.get_id()
        self.client_id = client.get_id()    
        self.minor = minor
        if minor:
            self.minor_id = minor.get_id()
        else:
            self.minor_id = None

    def __repr__(self) -> str:
        if self.is_cancelled:
            return f"Booking {self.id} for {self.client.get_name()} in {self.offering} and is cancelled"
        return f"Booking {self.id} is {self.offering.status} for {self.client} in {self.offering} and is not cancelled"
    
    def repr_client(self):
        return (
            f"\nBooking ID: {self.id}\n"
            f"Offering: {self.offering.get_lesson().get_type().value}\n"
            f"Location: {self.offering.get_lesson().get_location().get_name()}, {self.offering.get_lesson().get_location().get_city()}\n"
            f"Timeslot: {self.offering.get_lesson().get_timeslot().get_day_of_week()}, {self.offering.get_lesson().get_timeslot().get_start_time()} - {self.offering.get_lesson().get_timeslot().get_end_time()}\n"
            f"Availble from {self.offering.get_lesson().get_timeslot().get_start_date()} to {self.offering.get_lesson().get_timeslot().get_end_date()}\n"
            f"Instructor: {self.offering.get_instructor().get_name()}\n"
            f"Client: {self.client.get_name()}\n"
            f"Activity: {self.offering.get_lesson().get_specialization().value}\n"
        )
    
    def repr_minor(self):
        return (
            f"\nBooking ID: {self.id}\n"
            f"Offering: {self.offering.get_id()}\n"
            f"Location: {self.offering.get_lesson().get_location().get_name()}, {self.offering.get_lesson().get_location().get_city()}\n"
            f"Timeslot: {self.offering.get_lesson().get_timeslot().get_day_of_week()}, {self.offering.get_lesson().get_timeslot().get_start_time()} - {self.offering.get_lesson().get_timeslot().get_end_time()}\n"
            f"Availble from {self.offering.get_lesson().get_timeslot().get_start_date()} to {self.offering.get_lesson().get_timeslot().get_end_date()}\n"
            f"Instructor: {self.offering.get_instructor().get_name()}\n"
            f"Guardian: {self.client.get_name()}\n"
            f"Minor: {self.minor.get_name()}\n"
            f"Activity: {self.offering.get_lesson().get_specialization().value}\n"

        )
    
    def get_id(self) -> int:
        return self.id
    
    def get_client(self):
        return self.client
    
    def get_client_id(self) -> int:
        return self.client_id
    
    def get_is_cancelled(self) -> bool:
        return self.is_cancelled
    
    def get_offering(self):
        return self.offering

    def get_minor_id(self):
        return self.minor_id
