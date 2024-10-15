from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.config import Base
from models import Schedule
from .SpaceType import SpaceType

# Location Model
class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    space_type: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    #city: Mapped['City'] = relationship("City", backref="location")
    #city_id: Mapped[int] = mapped_column(Integer, ForeignKey('cities.id'), nullable=False)
    schedule: Mapped["Schedule"] = relationship("Schedule", back_populates="location", uselist=False)
    offerings: Mapped[list["Offering"]] = relationship("Offering", back_populates="location")

    def __init__(self, name: str, address: str, capacity: int, city: str, space_type: list[SpaceType]):
        self.name = name
        self.space_type = [space.value for space in space_type]
        self.address = address
        self.capacity = capacity
        self.city = city
        self.offerings = []
        self.schedule = Schedule(self, self.id)

    def get_schedule(self):
        return self.schedule
    
    def get_id(self) -> int:   
        return self.id
    
    def get_capacity(self) -> int:
        return self.capacity

    def __repr__(self):
        return f"Location {self.id} {self.name} ({self.address}), has a capacity of {self.capacity} and is located in {self.city}"