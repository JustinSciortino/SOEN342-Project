from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship
from config import Base
import enum

# Enum for lesson types
class LessonType(enum.Enum):
    group = "group"
    private = "private"

# Enum for user roles
class UserRole(enum.Enum):
    admin = "admin"
    client = "client"
    instructor = "instructor"

# User Model (Parent class for Client and Instructor)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    role = Column(Enum(UserRole), nullable=False)
    
    # Relationships
    instructor = relationship("Instructor", back_populates="user", uselist=False)
    client = relationship("Client", back_populates="user", uselist=False)

# Instructor Model
class Instructor(Base):
    __tablename__ = "instructors"

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    specialization = Column(String, nullable=False)
    availability = Column(String, nullable=False)  # Availability can be stored as JSON or a string pattern

    # Relationships
    user = relationship("User", back_populates="instructor")
    lessons = relationship("Lesson", back_populates="instructor")

# Client Model
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    guardian_name = Column(String, nullable=True)  # For underage clients
    guardian_phone = Column(String, nullable=True)

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
    lessons = relationship("Lesson", back_populates="schedule")

# Lesson Model
class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(LessonType), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    schedule_id = Column(Integer, ForeignKey('schedules.id'), nullable=False)
    instructor_id = Column(Integer, ForeignKey('instructors.id'), nullable=True)

    # Relationships
    schedule = relationship("Schedule", back_populates="lessons")
    instructor = relationship("Instructor", back_populates="lessons")
    bookings = relationship("Booking", back_populates="lesson")

# Booking Model
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    booked_at = Column(DateTime, nullable=False)

    # Relationships
    lesson = relationship("Lesson", back_populates="bookings")
    client = relationship("Client", back_populates="bookings")
