from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.config import Base

# Location Model
class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    #city: Mapped['City'] = relationship("City", backref="location")
    #city_id: Mapped[int] = mapped_column(Integer, ForeignKey('cities.id'), nullable=False)
    schedule: Mapped["Schedule"] = relationship("Schedule", back_populates="location", uselist=False)
    offerings: Mapped[list["Offering"]] = relationship("Offering", back_populates="location")