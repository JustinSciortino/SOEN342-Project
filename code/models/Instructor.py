
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column, Session
from database import Base
from models import User

# Instructor Model
class Instructor(User):
    __tablename__ = "instructors"

    id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True, autoincrement=True)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    specialization: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False) #! To be fixed needs to use the Specialization Enum
    available_cities: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    offerings: Mapped[list["Offering"]] = relationship("Offering", back_populates="instructor")

    __mapper_args__ = {
        "polymorphic_identity": "instructor",
    }

    def __init__(self, name: str, password: str, phone_number: str, specialization: list[str], available_cities: list[str]):
        super().__init__(name=name, password=password, type="instructor")
        self.phone_number = phone_number
        self.specialization = specialization
        self.available_cities = available_cities
        self.offerings = []

    def __repr__(self) -> str:
        return f"Instructor {self.id} {self.name} ({self.phone_number}), has the following specilizations: {self.specialization} and the following cities: {self.available_cities}"
    
    def instructor_menu(self, db:Session):
        from catalogs import UsersCatalog, LocationsCatalog
        instructor_menu_options = """
        Instructor Options:
        1. Select Offering
        2. View my Offerings
        3. Modify my Offering
        4. Modify my Account
        5. Logout and return to main menu
        """
        print(instructor_menu_options)