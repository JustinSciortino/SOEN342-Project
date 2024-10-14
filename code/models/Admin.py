from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.config import Base
from models import User
# Admin Model
class Admin(User):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True, autoincrement=True)

    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }

    def __init__(self, name: str, password: str):
        super().__init__(name=name, password=password, type="admin")

    def __repr__(self) -> str:
        return f"Admin {self.id} {self.name}"