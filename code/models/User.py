from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
from abc import abstractmethod

class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str]

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": "type",
    }

    def __init__(self, name: str, password: str, type: str):
        self.name = name
        self.password = password
        self.type = type
    
    @abstractmethod
    def get_type(self):
        return self.type
    
    @abstractmethod
    def get_id(self):
        return self.id
    
    @abstractmethod
    def get_name(self):
        return self.name   