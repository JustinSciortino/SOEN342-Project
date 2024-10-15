from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.config import Base
from models import Offering, Client

# Booking Model
class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client: Mapped["Client"] = relationship("Client", back_populates="bookings")
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey('clients.id'))
    status: Mapped[str] = mapped_column(String, default="Available")
    active: Mapped[str] = mapped_column(String, default=True)
    is_cancelled: Mapped[bool] = mapped_column(Boolean, default=False)
    offering_id: Mapped[int] = mapped_column(Integer, ForeignKey('offerings.id'))
    offering: Mapped["Offering"] = relationship("Offering", back_populates="bookings")

    def __init__(self, client: Client, status: str, active: str, is_cancelled: bool, offering: Offering):
        self.client = client
        self.status = status
        self.active = active
        self.is_cancelled = is_cancelled
        self.offering = offering
        self.offering_id = offering.get_id()
        self.client_id = client.get_id()    

    def __repr__(self) -> str:
        return f"Booking {self.id} is {self.status} for {self.client} in {self.offering}"
    
    def get_id(self) -> int:
        return self.id
    
    def get_client(self):
        return self.client
    
    def get_status(self) -> str:
        return self.status  
    
    def get_active(self) -> str:
        return self.active
    
    def get_is_cancelled(self) -> bool:
        return self.is_cancelled
    
    def get_offering(self):
        return self.offering

