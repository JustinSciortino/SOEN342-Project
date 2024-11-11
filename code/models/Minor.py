from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base

class Minor(Base):
    __tablename__ = "minors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    guardian = relationship("Client", back_populates="minors")
    guardian_id: Mapped[int] = mapped_column(Integer, ForeignKey('clients.id'), nullable=False)
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="minor")
    relationship_with_guardian: Mapped[str] = mapped_column(String, nullable=False)

    def __init__(self, guardian, name: str, age: int, relationship_with_guardian: str):
        self.name = name
        self.age = age
        self.guardian = guardian
        self.guardian_id = guardian.get_id()
        self.relationship_with_guardian = relationship_with_guardian

    def __repr__(self) -> str:
        return f"\nMinor {self.name}, {self.age} years old, Relationship: {self.relationship_with_guardian}"
    
    def get_id(self) -> int:
        return self.id
    
    def get_name(self) -> str:
        return self.name
    
    def get_age(self) -> int:
        return self.age
    
    def get_guardian(self):
        return self.guardian
    
    def get_relationship_with_guardian(self) -> str:
        return self.relationship_with_guardian