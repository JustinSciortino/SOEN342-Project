from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column, Session
from database.config import Base
from models import User, SpaceType


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
    
    def admin_menu(self, db: Session):
        from catalogs import UsersCatalog, LocationsCatalog, OfferingsCatalog
        locations_catalog = LocationsCatalog.get_instance(db)
        users_catalog = UsersCatalog.get_instance(db)  
        offerings_catalog = OfferingsCatalog.get_instance(db)

        admin_menu_options = """
        Admin Options:
        1. View Offerings
        2. Create Offering
        3. Modify Offering
        4. Cancel Offering
        5. Delete Client/Instructor Account
        6. View Client Bookings
        7. Add Location
        8. Modify Location
        9. View Location Schedule
        10. Delete Location
        11. Get All Locations
        12. Get Location based on City and optionally Name and Address
        13. Logout and return to main menu"""

        while True:
            print(admin_menu_options)
            choice = int(input("\nSelect an option: "))

            if choice == 1:
                pass

            if choice == 2:
                pass

            if choice == 3:
                pass

            if choice == 4:
                pass

            if choice == 5:
                print("\n--------Delete Client/Instructor Account--------")
                account_name = None
                _quit = False

                while True:
                    account_name = str(input("Enter the name of the account to delete (or 'q' to quit): "))
                    if account_name.lower() == 'q':
                        _quit = True
                        break
                    if not account_name:
                        print("Name cannot be empty. Please try again.")
                        continue
                    break

                if _quit == False:
                    try:
                        users_catalog.delete_user(account_name)
                    except ValueError as e:
                        print(f"{e} - The account was not deleted and you will be redirected to the main menu")
                        continue
                    print(f"Account {account_name} has been successfully deleted.")
                else:
                    print("\nYou will be redirected back to the admin menu.")

            if choice == 6:
                pass

            if choice == 7:
                print("\n--------Add Location--------")
                location_name = None
                location_address = None
                location_capacity = None
                location_city = None
                location_space_type = None
                _quit = False

                while True:
                    location_name = str(input("Enter location name (or 'q' to quit): "))
                    if location_name.lower() == 'q':
                        _quit = True
                        break
                    if not location_name:
                        print("Name cannot be empty. Please try again.")
                        continue
                    break

                if _quit == False:
                    while True:
                        location_address = str(input("Enter location address (or 'q' to quit): "))
                        if location_address.lower() == 'q':
                            _quit = True
                            break
                        if not location_address:
                            print("Address cannot be empty. Please try again.")
                            continue
                        break
                
                if _quit == False:
                    while True:
                        location_capacity = str(input("Enter location capacity (or 'q' to quit): "))
                        if location_capacity.lower() == 'q':
                            _quit = True
                            break
                        if not location_capacity:
                            print("Capacity cannot be empty. Please try again.")
                            continue
                        break
                    location_capacity = int(location_capacity)
                
                if _quit == False:
                    while True:
                        location_city = str(input("Enter location city (or 'q' to quit): "))
                        if location_city.lower() == 'q':
                            _quit = True
                            break
                        if not location_city:
                            print("City cannot be empty. Please try again.")
                            continue
                        break
                
                if _quit == False:
                    while True:
                        print(f"Available space types: {[space_type.value for space_type in SpaceType]}")
                        space_type_input = input("Enter location space type (e.g., 'rink', 'field', etc.)(or 'q' to quit): ").lower()
                        if space_type_input == 'q':
                            _quit = True
                            break
                
                        try:
                            location_space_type = SpaceType(space_type_input)
                        except ValueError:
                            print("Invalid space type. Please enter a valid option from the list.")
                            continue
                        break
                
                if _quit == False:
                    try:
                        location = locations_catalog.create_location(location_name, location_address, location_capacity, location_city, location_space_type)
                    except ValueError as e:
                        print(f"{e} - The location was not created and you will be redirected to the main menu")
                        continue
                    print(f"Location {location.get_name()} has been successfully created.")
                else:
                    print("\nYou will be redirected back to the admin menu.")

            if choice == 8:
                pass

            if choice == 9:
                pass

            if choice == 10:
                location_city = None
                location_name = None
                location_address = None
                _quit = False

                while True:
                    location_city = str(input("Enter location city (or 'q' to quit): "))
                    if location_city.lower() == 'q':
                        _quit = True
                        break
                    if not location_city:
                        print("City cannot be empty. Please try again.")
                        continue
                    break

                if _quit == False:
                    while True:
                        location_name = str(input("Enter location name (or 'q' to quit): "))
                        if location_name.lower() == 'q':
                            _quit = True
                            break
                        if not location_name:
                            print("Name cannot be empty. Please try again.")
                            continue
                        break

                if _quit == False:
                    while True:
                        location_address = str(input("Enter location address (or 'q' to quit): "))
                        if location_address.lower() == 'q':
                            _quit = True
                            break
                        if not location_address:
                            print("Address cannot be empty. Please try again.")
                            continue
                        break

                if _quit == False:
                    try:
                        locations_catalog.delete_location(location_city, location_name, location_address)  
                    except ValueError as e:
                        print(f"{e} - The location was not deleted.")
                        continue
                    print(f"Location {location_name} has been successfully deleted.")
                else:
                    print("\nYou will be redirected back to the admin menu.")

            if choice == 11:
                pass

            if choice == 12:
                print("\n--------Get Location based on City and optionally Name and Address--------")
                location_city = None
                location_name = None
                location_address = None
                _quit = False

                while True:
                    location_city = str(input("Enter location city (or 'q' to quit): "))
                    if location_city.lower() == 'q':
                        _quit = True
                        break
                    if not location_city:
                        print("City cannot be empty. Please try again.")
                        continue
                    break

                if _quit == False:
                    location_name = str(input("Enter location name (optional - click Enter to not add a name)(or 'q' to quit): "))
                    if location_name.lower() == 'q':
                        _quit = True
                        break
                if _quit == False:
                    location_address = str(input("Enter location address (optional - click Enter to not add an address)(or 'q' to quit): "))
                    if location_address.lower() == 'q':
                        _quit = True
                        break
                
                if _quit == False:
                    if location_name and location_address:
                        try:
                            location = locations_catalog.get_location(city=location_city, name=location_name, address=location_address)
                            print('\n',location)
                        except ValueError as e:
                            print(f"{e} - The location was not found.")
                            continue    
                    else:
                        try:
                            location = locations_catalog.get_location(city=location_city)
                            print('\n',location)
                        except ValueError as e:
                            print(f"{e} - The location was not found.")
                            continue
                else:
                    print("\nYou will be redirected back to the admin menu.")

            if choice == 13:
                return