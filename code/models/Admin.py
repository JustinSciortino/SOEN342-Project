from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.config import Base

# Admin Model
class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True, autoincrement=True)

    __mapper_args__ = {
        "polymorphic_identity": "Admin",
    }