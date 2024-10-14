
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base

# Instructor Model
class Instructor(Base):
    __tablename__ = "instructors"

    id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True, autoincrement=True)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    specialization: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    available_cities: Mapped[list["City"]] = relationship("City", backref="instructor", nullable=False)
    offerings: Mapped[list["Offering"]] = relationship("Offering", back_populates="instructor")

    __mapper_args__ = {
        "polymorphic_identity": "Instructor",
    }

    def __init__(self):
        self.offerings = []

    def __repr__(self) -> str:
        return f"Instructor {self.id} {self.name} ({self.phone_number}), has the following specilizations: {self.specialization}"