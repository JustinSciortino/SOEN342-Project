from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship
from db.config import Base

# Admin Model
class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, ForeignKey('users.id'), primary_key=True, autoincrement=True)

    # Relationships
    user = relationship("User", back_populates="admin")