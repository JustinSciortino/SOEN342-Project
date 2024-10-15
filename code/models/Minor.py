from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base

class Minor(Base):
    __tablename__ = "minors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    guardian = relationship("Client", back_populates="minor")

    def __init__(self, guardian: Client, name: str, age: int):
        self.name = name
        self.age = age
        self.guardian = guardian

    def __repr__(self) -> str:
        return f"Minor {self.name} is {self.age} years old"
    
    def get_id(self) -> int:
        return self.id
    
    def get_name(self) -> str:
        return self.name
    
    def get_age(self) -> int:
        return self.age
    
    def get_guardian(self):
        return self.guardian