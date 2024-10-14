
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
from models import User

# Instructor Model
class Instructor(User):
    __tablename__ = "instructors"

    id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True, autoincrement=True)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    specialization: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    available_cities: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    offerings: Mapped[list["Offering"]] = relationship("Offering", back_populates="instructor")

    __mapper_args__ = {
        "polymorphic_identity": "instructor",
    }

    def __init__(self, name: str, password: str, phone_number: str, specialization: list[str], available_cities: list[str]):
        super().__init__(name=name, password=password, type="instructor")
        self.phone_number = phone_number
        self.specialization = specialization
        self.available_cities = available_cities
        self.offerings = []

    def __repr__(self) -> str:
        return f"Instructor {self.id} {self.name} ({self.phone_number}), has the following specilizations: {self.specialization} and the following cities: {self.available_cities}"