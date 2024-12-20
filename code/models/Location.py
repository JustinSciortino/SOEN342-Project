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
    schedule: Mapped["Schedule"] = relationship("Schedule", back_populates="location", uselist=False, cascade="all, delete-orphan")
    lessons: Mapped[list["Lesson"]] = relationship("Lesson", back_populates="location")

    def __init__(self, name: str, address: str, capacity: int, city: str, space_type: list[SpaceType]):
        self.name = name
        self.space_type = [space.value for space in space_type]
        self.address = address
        self.capacity = capacity
        self.city = city #! May want to do .lower() and search for all cities in lowercase
        self.offerings = []
        self.schedule = Schedule(self, self.id)

    def get_schedule(self):
        return self.schedule
    
    def get_id(self) -> int:   
        return self.id
    
    def get_capacity(self) -> int:
        return self.capacity
    
    def get_space_type(self):
        return self.space_type

    def get_name(self) -> str:
        return self.name
    
    def get_address(self) -> str:
        return self.address
    
    def get_city(self) -> str:
        return self.city

    def __repr__(self):
        return (
            f"\nLocation ID: {self.id}\n"
            f"Location: {self.name}, {self.address} {self.city}\n"
            f"Capacity: {self.capacity}\n"
            f"Space Type: {self.space_type}\n"
        )
    
    def offering_repr(self):
        return f"Location {self.id} {self.name} ({self.address}), located in {self.city}"