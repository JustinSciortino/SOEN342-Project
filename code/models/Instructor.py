
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column, Session
from database import Base
from models import User, SpecializationType

# Instructor Model
class Instructor(User):
    __tablename__ = "instructors"

    id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True, autoincrement=True)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    specialization: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False) 
    #specialization = mapped_column(ARRAY(Enum(SpecializationType)), nullable=False)
    available_cities: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    offerings: Mapped[list["Offering"]] = relationship("Offering", back_populates="instructor")

    __mapper_args__ = {
        "polymorphic_identity": "instructor",
    }

    def __init__(self, name: str, password: str, phone_number: str, specialization: list[SpecializationType], available_cities: list[str]):
        super().__init__(name=name, password=password, type="instructor")
        self.phone_number = phone_number
        self.specialization = [spec.value for spec in specialization]
        self.available_cities = available_cities
        self.offerings = []

    def __repr__(self) -> str:
        return f"Instructor {self.id} {self.name} ({self.phone_number}), has the following specilizations: {self.specialization} and the following cities: {self.available_cities}"
    
def instructor_menu(self, db: Session):
    from catalogs import OfferingsCatalog, UsersCatalog
    offerings_catalog = OfferingsCatalog.get_instance(db)
    users_catalog = UsersCatalog.get_instance(db)

    instructor_menu_options = """
    Instructor Options:
    1. Select Offering
    2. View my Offerings
    3. Modify my Offering
    4. Modify my Account
    5. Logout and return to main menu
    """

    while True:
        choice = None
        while True:
            print(instructor_menu_options)
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
            print("\n--------Select Offering--------")
            offerings = offerings_catalog.get_available_offerings_for_instructor(self)

            if not offerings:
                print("No available offerings found that match your criteria.")
            else:
                print("\nAvailable Offerings:")
                for offering in offerings:
                    print(offering.repr_instructor())  #

                selected_offering_id = None
                while True:
                    selected_offering_id = input("\nEnter the ID of the offering you want to select (or 'q' to quit): ")
                    if selected_offering_id.lower() == 'q':
                        return  
                    try:
                        selected_offering_id = int(selected_offering_id)
                        selected_offering = next((off for off in offerings if off.id == selected_offering_id), None)
                        if selected_offering:
                            if self.has_time_conflict(selected_offering):
                                print("You cannot book this offering because it conflicts with an existing offering.")
                            else:
                                selected_offering.instructor_id = self.id
                                self.offerings.append(selected_offering)
                                try:
                                    db.commit()  
                                    print(f"Successfully selected offering with ID {selected_offering.id} and assigned it to you.")
                                except Exception as e:
                                    db.rollback()  
                                    print(f"Error: {e}. Could not update offering.")
                            break
                        else:
                            print("Invalid offering ID. Please select a valid offering from the list.")
                    except ValueError:
                        print("Invalid input. Please enter a valid offering ID.")



        if choice == 2:
            print("\n--------View my Offerings--------")
            my_offerings = offerings.get_offerings_by_instructor_id(self.id)
            if not my_offerings:
                print("You have no offerings.")
            else:
                print("\nYour Offerings:")
                for offering in my_offerings:
                    print(offering.repr_instructor()) 

        if choice == 3:
            print("\n--------Modify my Offering (Remove Myself)--------")

            my_offerings = offerings_catalog.get_offerings_by_instructor_id(self.id)

            if not my_offerings:
                print("You have no offerings to modify.")
            else:
                print("\nYour Offerings:")
                for offering in my_offerings:
                    print(offering.repr_instructor())  

                selected_offering_id = None
                while True:
                    selected_offering_id = input("\nEnter the ID of the offering you want to remove yourself from (or 'q' to quit): ")
                    if selected_offering_id.lower() == 'q':
                        return  
                    try:
                        selected_offering_id = int(selected_offering_id)
                        selected_offering = next((off for off in my_offerings if off.id == selected_offering_id), None)
                        if selected_offering:
                            break
                        else:
                            print("Invalid offering ID. Please select a valid offering from the list.")
                    except ValueError:
                        print("Invalid input. Please enter a valid offering ID.")

                selected_offering.instructor_id = None
                self.offerings.remove(selected_offering)  
                
                try:
                    db.commit()  
                    print(f"You have successfully removed yourself from offering with ID {selected_offering.id}.")
                except Exception as e:
                    db.rollback()  
                    print(f"Error: {e}. Could not update the offering.")

        if choice == 4:
            print("\n--------Modify my Account--------")

            print(f"\nCurrent Account Details:\n"
                f"Name: {self.name}\n"
                f"Phone Number: {self.phone_number}\n"
                f"Specialization: {self.specialization}\n"
                f"Available Cities: {self.available_cities}")

            _quit = False

            print("\nPlease enter the new information for your account. Press 'enter' to keep the current information.")

            new_name = input(f"\nEnter new name (current: {self.name}) or 'q' to quit: ")
            if new_name.lower() != 'q' and new_name:
                self.name = new_name

            if not _quit:
                new_phone = input(f"Enter new phone number (current: {self.phone_number}) or 'q' to quit: ")
                if new_phone.lower() != 'q' and new_phone:
                    self.phone_number = new_phone

            if not _quit:
                new_password = input("Enter new password or 'q' to quit: ")
                if new_password.lower() != 'q' and new_password:
                    self.password = new_password 

            if not _quit:
                new_specializations_input = input(
                    f"Enter new specializations separated by commas (current: {', '.join(self.specialization)}) or 'q' to quit: "
                ).strip()

                if new_specializations_input.lower() == 'q':
                    _quit = True
                elif new_specializations_input:
                    try:
                        # Assuming SpecializationType enums are case-insensitive or matching input format
                        new_specializations = [
                            SpecializationType(spec.strip().capitalize()) for spec in new_specializations_input.split(",")
                        ]
                        # Assigning enum members directly, adjust if you need their .value instead
                        self.specialization = [spec.value for spec in new_specializations]
                    except ValueError as e:
                        print("Invalid specialization input. No changes made to specialization.")

            if not _quit:
                try:
                    db.commit() 
                    print("Account details have been successfully updated.")
                except Exception as e:
                    db.rollback()  
                    print(f"Error: {e}. Could not update the account details.")
            else:
                print("No changes were made to the account.")


        if choice == 5:
            print("\nLogging out...")
            return
