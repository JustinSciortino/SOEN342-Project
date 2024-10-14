# User Model (Parent class for Client and Instructor)
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship
from db.config import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Relationships
    instructor = relationship("Instructor", back_populates="user", uselist=False)
    client = relationship("Client", back_populates="user", uselist=False)
    admin = relationship("Admin", back_populates="user", uselist=False)