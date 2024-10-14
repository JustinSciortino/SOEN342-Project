
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship
from db.config import Base

# Instructor Model
class Instructor(Base):
    __tablename__ = "instructors"

    id = Column(Integer, ForeignKey('users.id'), primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    specialization = Column(String, nullable=False)
    availabl_cities = Column(String, nullable=False)  # Availability can be stored as JSON or a string pattern

    # Relationships
    user = relationship("User", back_populates="instructor")
    offerings = relationship("Offering", back_populates="instructor")
