from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column, Session
from database import Base
from models import Minor, User, Booking, SpecializationType
from typing import List




class Client(User):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True, autoincrement=True)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    minors: Mapped[list["Minor"]] = relationship("Minor", back_populates="guardian", cascade="all, delete-orphan")
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="client", cascade="all, delete-orphan") #! Test to make sure they actually get deleted if Client is deleted


    __mapper_args__ = {
        "polymorphic_identity": "client",
    }

    def __init__(self, name: str, password: str, phone_number: str):
        super().__init__(name=name, password=password, type="client")
        self.phone_number = phone_number
        self.bookings = []

    def __repr__(self) -> str:
        if self.minors:
            minors_names = ", ".join(minor.name for minor in self.minors)
            return f"Client {self.id}, {self.name}, ({self.phone_number}), legal guardian of: {minors_names}"
        else:
            return f"Client {self.id}, {self.name}, ({self.phone_number}), no minors associated"

    
    def get_id(self) -> int:
        return self.id
    
    def get_phone_number(self) -> str:
        return self.phone_number
    
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
        1. View Offerings (Available and Not Available)
        2. Book an Available Offering
        3. View My Bookings
        4. Cancel a Booking
        5. View Minor's Bookings (Only for Legal Guardians)
        6. Logout and return to main menu
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
                    if choice not in range(1, 7):
                        print("Invalid choice. Please enter a number between 1 and 6.")
                        continue
                    break
                except ValueError:
                    print("Invalid choice. Please enter a valid number.")
                    continue

            if choice == 1:
                print("\n--------View Offerings (Available and Not Available)--------")
                _quit = False

                offering_city = input("Enter offering city (or 'q' to quit or click 'enter' to not add a city): ").strip() or None

                if offering_city is not None:
                    if offering_city.lower() == 'q':
                        _quit = True
                    else:
                        offering_city = offering_city.capitalize()

                if not _quit:
                    from models import SpecializationType
                    valid_specializations = [spec.value for spec in SpecializationType]
                    print(f"Available specialization types: {valid_specializations}")
                    
                    while True:
                        offering_specialization = input("Enter offering specialization (or 'q' to quit or press 'Enter' to skip): ").strip() or None
                        
                        if offering_specialization is None:
                            break

                        if offering_specialization.lower() == 'q':
                            _quit = True
                            break
                        elif offering_specialization not in valid_specializations:
                            print("Invalid specialization. Please enter a valid specialization from the list.")
                            continue
                        else:
                            offering_specialization = SpecializationType(offering_specialization)
                            break

                if not _quit:
                    from models import LessonType
                    valid_types = [offering_type.value for offering_type in LessonType]
                    print(f"Available offering types: {valid_types}")
                    
                    while True:
                        offering_type = input("Enter offering type (or 'q' to quit or press 'Enter' to skip): ").strip() or None
                        
                        if offering_type is None:
                            # Skip adding an offering type if Enter is pressed without input
                            break

                        if offering_type.lower() == 'q':
                            _quit = True
                            break
                        elif offering_type not in valid_types:
                            print("Invalid offering type. Please enter a valid type from the list.")
                            continue
                        else:
                            offering_type = LessonType(offering_type)
                            break


                if not _quit:
                    offerings = offerings_catalog.get_offerings(city=offering_city, specialization=offering_specialization, _type=offering_type)
                    if not offerings:
                        print("No offerings at the moment")
                    else:
                        print("\nOfferings:")
                        for offering in offerings:
                            is_booked = False
                            for booking in self.get_bookings():
                                if booking.get_offering().get_id() == offering.get_id():
                                    print(offering.repr_client_booked())
                                    is_booked = True
                                    break 

                            if not is_booked:
                                print(offering.repr_client())
                else:
                    print("\nYou will be redirected back to the client menu.")
                    continue

                    
            if choice == 2:
                print("\n--------Book an Available Offering--------")
                from models import SpecializationType

                specializations = [spec.value for spec in SpecializationType]
                print("\nSpecializations Offered:")
                for idx, spec in enumerate(specializations, start=1):
                    print(f"{idx}. {spec}")

                while True:
                    specialization_choice = input("\nSelect the number corresponding to the specialization you'd like to search for: ").strip()
                    
                    try:
                        specialization_choice = int(specialization_choice)
                        if 1 <= specialization_choice <= len(specializations):
                            chosen_specialization = SpecializationType(specializations[specialization_choice - 1])
                            break  # Exit loop if the selection is valid
                        else:
                            print(f"Invalid selection. Please enter a number between 1 and {len(specializations)}.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number corresponding to a specialization.")

                offerings = offerings_catalog.get_available_offerings(specialization=chosen_specialization)
                available_offerings = []

                #! Needs to be tested
                for offering in offerings:
                    is_booked = False
                    for booking in self.get_bookings():
                        if booking.get_offering().get_id() == offering.get_id():
                            is_booked = True
                            break
                    if not is_booked:
                        available_offerings.append(offering)

                if not available_offerings:
                    print(f"No available offerings for {chosen_specialization.value} at this time.")
                else:

                    #! Need to double check a new booking doesnt conflict with an existing booking they have
                    print(f"\nAvailable Offerings for {chosen_specialization.value}:")
                    for offering in available_offerings:
                        print(offering.repr_client()) 

                    offering_id = input("\nEnter the ID of the offering you'd like to book (or enter to skip): ").strip()

                    selected_offering = next((offering for offering in available_offerings if str(offering.id) == offering_id), None)

                    if selected_offering:
                        is_booking_for_minor = input("Is this booking for a minor? (yes/no): ").lower().strip()

                        if is_booking_for_minor == 'yes':
                            minor_id = None
                            if self.minors is not None:
                                print("\nYour Minors:")
                                for minor in self.minors:
                                    print(minor.__repr__())
                                minor_id = input("\nIf the booking is for one of the above minors, enter their id, if not and you want to create a new minor, enter 'No': ").strip()
                                if minor_id != 'No':
                                    selected_minor = next((minor for minor in self.minors if str(minor.id) == minor_id), None)
                                    if not selected_minor:
                                        print("Invalid minor ID.")
                                        break
                                    bookings_catalog.create_booking(self, selected_offering, minor=selected_minor)
                                else:
                                    minor_name = input("Enter minor's name: ").strip()
                                    minor_age = input("Enter minor's age: ").strip()
                                    minor_relationship = input("Enter your relationship with the minor (daughter, son, grandchild, sibling, etc): ").strip()
                                    from catalogs import UsersCatalog
                                    users_catalog = UsersCatalog.get_instance(db)
                                    minor = users_catalog.create_minor(self, minor_name, minor_age, minor_relationship)
                                    bookings_catalog.create_booking(self, selected_offering, minor=minor)
                        else:
                            bookings_catalog.create_booking(self, selected_offering)

                    else:
                        print("Invalid offering ID.") #! Loop until they enter a valid offering ID or add a quit option

            if choice == 3:
                print("\n--------View My Bookings--------")

                client_bookings = bookings_catalog.get_client_bookings(self)    
                if not client_bookings:
                    print("You have no bookings.")
                else:
                    has_bookings = False
                    print("\nYour Bookings:")
                    for booking in client_bookings:
                        if booking.get_minor_id() is None:
                            has_bookings = True
                            print(booking.repr_client())
                    if has_bookings == False:
                        print("You have personally have no bookings. Check to see if you have bookings for your minors.")

            if choice == 4:
                print("\n--------Cancel a Booking--------")

                client_bookings = bookings_catalog.get_client_bookings(self)

                if not client_bookings:
                    print("\nYou have no bookings to cancel.")
                else:
                    print("\nYour Current Bookings:")
                    for booking in client_bookings:
                        if booking.get_minor_id() is not None:
                            print(booking.repr_minor())
                        else:
                            print(booking.repr_client())  

                    booking_id = input("\nEnter the ID of the booking you'd like to cancel: ").strip()

                    selected_booking = next((booking for booking in client_bookings if str(booking.id) == booking_id), None)

                    if not selected_booking:
                        print("Invalid booking ID.")
                        continue

                    bookings_catalog.cancel_booking(selected_booking)
                    print("Booking successfully cancelled.")


            if choice == 5:
                print("\n--------View Minor's Bookings--------")

                if not self.minors:  # Check if the list of minors is empty
                    print("You do not have any minors associated with your account. Redirecting back to the client menu.")
                    continue
                
                # Display the user's minors
                print("\nYour Minors:")
                for minor in self.minors:
                    print(minor.__repr__())

                guardian_bookings = bookings_catalog.get_client_bookings(self)
                
                has_minor_bookings = False
                for booking in guardian_bookings:
                    if booking.get_minor_id() is not None:
                        print(booking.repr_minor())
                        has_minor_bookings = True
                
                if not has_minor_bookings:
                    print("\nYou have no bookings for your minors.")


            if choice == 6:
                print("\nLogging out...")
                return
    