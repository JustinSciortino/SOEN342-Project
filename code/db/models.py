from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship
from db.config import Base
import enum

# Enum for offering types
class OfferingType(enum.Enum):
    group = "group"
    private = "private"

# User Model (Parent class for Client and Instructor)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    
    # Relationships
    instructor = relationship("Instructor", back_populates="user", uselist=False)
    client = relationship("Client", back_populates="user", uselist=False)
    admin = relationship("Admin", back_populates="user", uselist=False)

# Admin Model
class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    # Relationships
    user = relationship("User", back_populates="admin")

# Instructor Model
class Instructor(Base):
    __tablename__ = "instructors"

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    specialization = Column(String, nullable=False)
    availabl_cities = Column(String, nullable=False)  # Availability can be stored as JSON or a string pattern

    # Relationships
    user = relationship("User", back_populates="instructor")
    offerings = relationship("Offering", back_populates="instructor")

# Client Model
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_underage = Column(Boolean, nullable=False)
    guardian_id = Column(String, nullable=True)  # For underage clients

    # Relationships
    user = relationship("User", back_populates="client")
    bookings = relationship("Booking", back_populates="client")

# Location Model
class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    room = Column(String, nullable=False)

    # Relationships
    schedules = relationship("Schedule", back_populates="location")

# Schedule Model (for time slots in locations)
class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    day_of_week = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    # Relationships
    location = relationship("Location", back_populates="schedules")
    offerings = relationship("Offering", back_populates="schedule")

# Offering Model
class Offering(Base):
    __tablename__ = "offerings"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(OfferingType), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    schedule_id = Column(Integer, ForeignKey('schedules.id'), nullable=False)
    instructor_id = Column(Integer, ForeignKey('instructors.id'), nullable=True)
    is_available = Column(Boolean, default=True)
    status = Column(String, default="Available")  # Adding status field to track offering state

    # Relationships
    schedule = relationship("Schedule", back_populates="offerings")
    instructor = relationship("Instructor", back_populates="offerings")
    bookings = relationship("Booking", back_populates="offering")

# Booking Model
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    offering_id = Column(Integer, ForeignKey('offerings.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    booked_at = Column(DateTime, nullable=False)

    # Relationships
    offering = relationship("Offering", back_populates="bookings")
    client = relationship("Client", back_populates="bookings")
