from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column, Session
from database import Base
from models import Minor, Booking   
from SpecializationType import SpecializationType



class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True, autoincrement=True)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    is_legal_guardian: Mapped[bool] = mapped_column(Boolean, nullable=False)
    minor: Mapped["Minor"] = relationship("Minor", back_populates="guardian")  # For underage clients
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="client")

    __mapper_args__ = {
        "polymorphic_identity": "client",
    }

    def __init__(self, phone_number: str, is_legal_guardian: bool, minor_name: str = None, minor_age: int = None):
        self.phone_number = phone_number
        self.is_legal_guardian = is_legal_guardian
        if is_legal_guardian:
            self.minor = Minor(self, minor_name, minor_age)
        else:
            self.minor = None
        self.bookings = []

    def __repr__(self) -> str:
        if self.is_legal_guardian:
            return f"Client {self.id} ({self.phone_number}) is a legal guardian of {self.minor}"
        return f"Client {self.id} ({self.phone_number}) is a client"
    
    def get_id(self) -> int:
        return self.id
    
    def get_phone_number(self) -> str:
        return self.phone_number
    
    def is_legal_guardian(self) -> bool:
        return self.is_legal_guardian
    
    def get_minor(self) -> Minor:  
        return self.minor
    
    def get_bookings(self) -> list["Booking"]:
        return self.bookings
    
    def client_menu(self, db: Session):
        from catalogs import OfferingsCatalog, BookingsCatalog
        bookings_catalog = BookingsCatalog.get_instance(db)  
        offerings_catalog = OfferingsCatalog.get_instance(db)

        client_menu_options = """
        Client Options:
        1. View Available Offerings (with Instructor)
        2. Book an Available Offering
        3. View My Bookings
        4. Cancel a Booking
        5. Logout and return to main menu
        """

        while True:
            choice = None
            while True:
                print(client_menu_options)
                choice = input("\nSelect an option: ")
                if choice.strip() == "":
                    print("Invalid choice. Please enter a number.")
                    continue

                try:
                    choice = int(choice)
                    if choice not in range(1, 6):
                        print("Invalid choice. Please enter a number between 1 and 5.")
                        continue
                    break
                except ValueError:
                    print("Invalid choice. Please enter a valid number.")
                    continue

            if choice == 1:
                print("\n--------View Offerings--------")
                
                offerings = offerings_catalog.get_offerings_with_instructor()
                for offering in offerings:
                    offering.update_status(self)


                if not offerings:
                    print("No available offerings with an instructor at this time.")
                else:
                    print("\nAvailable Offerings:")
                    for offering in offerings:
                        print(offering.repr_client())  

            if choice == 2:
                print("\n--------Book an Available Offering--------")

                specializations = [spec.value for spec in SpecializationType]
                print("\nSpecializations Offered:")
                for idx, spec in enumerate(specializations, start=1):
                    print(f"{idx}. {spec}")

                specialization_choice = input("\nSelect the number corresponding to the specialization you'd like to search for: ").strip()

                try:
                    specialization_choice = int(specialization_choice)
                    if specialization_choice < 1 or specialization_choice > len(specializations):
                        raise ValueError
                    chosen_specialization = SpecializationType(specializations[specialization_choice - 1])
                except ValueError:
                    print("Invalid selection. Please enter a valid number corresponding to a specialization.")
                    return
                
                offerings = offerings_catalog.get_offerings_with_instructor()
                for offering in offerings:
                    offering.update_status(self)

                available_offerings = [
                    offering for offering in offerings
                    if offering.specialization == chosen_specialization and offering.status == "Available"
                ]

                if not available_offerings:
                    print(f"No available offerings for {chosen_specialization.value} at this time.")
                else:
                    print(f"\nAvailable Offerings for {chosen_specialization.value}:")
                    for offering in available_offerings:
                        print(offering.repr_client(self)) 

                    offering_id = input("\nEnter the ID of the offering you'd like to book: ").strip()

                    selected_offering = next((offering for offering in available_offerings if str(offering.id) == offering_id), None)

                    if selected_offering:
                        bookings_catalog.create_booking(self, selected_offering)
                    else:
                        print("Invalid offering ID.")

            if choice == 3:
                print("\n--------View My Bookings--------")
                bookings_catalog = BookingsCatalog.get_instance(db)

                client_bookings = bookings_catalog.get_client_bookings(self)    
                if not client_bookings:
                    print("You have no bookings.")
                else:
                    print("\nYour Bookings:")
                    for booking in client_bookings:
                        print(booking.repr_client())

            if choice == 4:
                print("\n--------Cancel a Booking--------")

                client_bookings = bookings_catalog.get_client_bookings(self)

                if not client_bookings:
                    print("You have no bookings to cancel.")
                    return

                print("\nYour Current Bookings:")
                for booking in client_bookings:
                    print(booking.repr_client())  

                booking_id = input("\nEnter the ID of the booking you'd like to cancel: ").strip()

                selected_booking = next((booking for booking in client_bookings if str(booking.id) == booking_id), None)

                if not selected_booking:
                    print("Invalid booking ID.")
                    return

                bookings_catalog.cancel_booking(self, selected_booking)

            if choice == 5:
                print("\nLogging out...")
                return
    