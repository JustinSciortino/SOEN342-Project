from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column, Session
from database.config import Base
from models import User, SpaceType, Offering
from .SpaceSpecializationMap import SPACE_SPECIALIZATION_MAP
import datetime


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
    
    def admin_get_location(self, db: Session):
        from catalogs import LocationsCatalog
        locations_catalog = LocationsCatalog.get_instance(db)
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

        if _quit == False:
            location_address = str(input("Enter location address (optional - click Enter to not add an address)(or 'q' to quit): "))
            if location_address.lower() == 'q':
                _quit = True
        
        if _quit == False:
            if location_name and location_address:
                try:
                    location = locations_catalog.get_location(city=location_city, name=location_name, address=location_address)
                    return location
                    print('\n',location)
                except ValueError as e:
                    print(f"{e} - The location was not found.")
                    return    
            else:
                try:
                    location = locations_catalog.get_location(city=location_city)
                    for l in location:
                        print('\n',l)
                except ValueError as e:
                    print(f"{e} - The location was not found.")
                    return
        else:
            print("\nYou will be redirected back to the admin menu.")
    
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
            choice = None
            while True:
                print(admin_menu_options)
                choice = input("\nSelect an option: ")
                if choice.strip() == "":
                    print("Invalid choice. Please enter a number.")
                    continue
                
                try:
                    choice = int(choice)
                    if choice not in range(1, 14):
                        print("\nInvalid choice. Please enter a number between 1 and 13.")
                        continue
                    break
                except ValueError:
                    print("\nInvalid choice. Please enter a valid number.")
                    continue


            if choice == 1:
                print("\n--------View Offerings--------")
                offering_city = None
                offering_space_type = None
                offering_type = None
                _quit = False


                offering_city = input("Enter offering city (or 'q' to quit or 'enter' to not add a city): ").strip() or None
                if offering_city is not None and offering_city.lower() == 'q':
                    _quit = True

                if _quit == False:
                    from models import SpaceType
                    print(f"Available space types: {[space_type.value for space_type in SpaceType]}")
                    offering_space_type = input("Enter offering space type (e.g., 'rink', 'field', etc.)(or 'q' to quit or 'enter' to not add a space type): ").strip() or None
                    if offering_space_type is not None and offering_space_type.lower() == 'q':
                        _quit = True
                
                if _quit == False:
                    from models import OfferingType
                    print(f"Available offering types: {[offering_type.value for offering_type in OfferingType]}")
                    offering_type = input("Enter offering type (or 'q' to quit or 'enter' to not add an offering type): ").strip() or None
                    if offering_type is not None and offering_type.lower() == 'q':
                        _quit = True

                if _quit == False:
                    offerings = offerings_catalog.get_all_offerings(city=offering_city, space_type=offering_space_type, _type=offering_type, is_admin=True)

                    if not offerings:
                        print("\nNo offerings found.")

                    for offering in offerings:
                        print(offering.repr_admin())

            if choice == 2:
                print("\n--------Create Offering--------")
                location_id = None
                _quit=False

                while True:
                    location_id = str(input("Enter location id (or 'q' to quit): "))
                    if location_id.lower() == 'q':
                        _quit = True
                        break
                    if not location_id:
                        print("Id cannot be empty. Please try again.")
                        continue
                    break
                location_id = int(location_id)
                
                location = locations_catalog.get_location_by_id(location_id)

                if location and _quit == False:
                    day_of_week = None
                    start_time = None
                    start_date = None
                    end_date = None
                    end_time = None

                    while True:
                        day_of_week = str(input("Enter day of the week (e.g., 'Monday', 'Tuesday', etc.)(or 'q' to quit): "))
                        if day_of_week.lower() == 'q':
                            _quit = True
                            break
                        if not day_of_week:
                            print("Day of the week cannot be empty. Please try again.")
                            continue
                        break
                    
                    if _quit == False:
                        while True:
                            start_time_str = input("Enter start time (e.g., '09:00')(or 'q' to quit): ")
                            if start_time_str.lower() == 'q':
                                _quit = True
                                break
                            if not start_time_str:
                                print("Start time cannot be empty. Please try again.")
                                continue
                            try:
                                start_time = datetime.datetime.strptime(start_time_str, "%H:%M").time()
                                break
                            except ValueError:
                                print("Invalid time format. Please use HH:MM format.")
                    
                    if _quit == False:
                        while True:
                            start_date_str = input("Enter start date (e.g., '2022-01-01')(or 'q' to quit): ")
                            if start_date_str.lower() == 'q':
                                _quit = True
                                break

                            if not start_date_str:
                                print("Start date cannot be empty. Please try again.")
                                continue

                            try:
                                start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
                                break
                            except ValueError:
                                print("Invalid date format. Please use YYYY-MM-DD format.")
                    
                    if _quit == False:
                        while True:
                            end_time_str = input("Enter end time (e.g., '09:00')(or 'q' to quit): ")
                            if end_time_str.lower() == 'q':
                                _quit = True
                                break
                            if not end_time_str:
                                print("End time cannot be empty. Please try again.")
                                continue
                            try:
                                end_time = datetime.datetime.strptime(end_time_str, "%H:%M").time()
                                if end_time <= start_time:
                                    print("End time must be after start time. Please try again.")
                                    continue
                                break
                            except ValueError:
                                print("Invalid time format. Please use HH:MM format.")

                    if _quit == False:
                        while True:
                            end_date_str = input("Enter end date (e.g., '2022-01-01')(or 'q' to quit): ")
                            if end_date_str.lower() == 'q':
                                _quit = True
                                break
                            if not end_date_str:
                                print("End date cannot be empty. Please try again.")
                                continue

                            try:
                                end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
                                if end_date < start_date:
                                    print("End date must be after start date. Please try again.")
                                    continue
                                break
                            except ValueError:
                                print("Invalid date format. Please use YYYY-MM-DD format.")
                    
                    if _quit == False:
                        from models import Timeslot
                        timeslot = Timeslot(day_of_week=day_of_week, start_time=start_time, start_date=start_date, end_time=end_time, end_date=end_date, schedule_id=location.get_schedule().get_id())
                        is_conflicting = location.get_schedule().is_conflicting(timeslot)

                        if is_conflicting:
                            print("Timeslot conflicts with existing timeslots. Offering cannot be created.")
                            continue

                        offering_type = None
                        offering_capacity = None
                        specialization = None

                        while True:
                            from models import OfferingType
                            print(f"Available offering types: {[offering_type.value for offering_type in OfferingType]}")
                            offering_type_input = input("Enter offering type (e.g. private or group)(or 'q' to quit): ").lower()
                            if offering_type_input == 'q':
                                _quit = True
                                break

                            if not offering_type_input:
                                print("Offering type cannot be empty. Please try again.")
                                continue

                            try:
                                offering_type = OfferingType(offering_type_input)
                            except ValueError:
                                print("Invalid offering type. Please enter a valid option from the list.")
                                continue
                            break

                        #!Incomplete
                        if _quit == False:
                            from models import SpecializationType, SPACE_SPECIALIZATION_MAP
                            print(f"Available offering types: {[offering_type.value for offering_type in OfferingType]}")

                        if _quit == False and offering_type == OfferingType.group:
                            while True:
                                offering_capacity = str(input("Enter offering capacity (or 'q' to quit): "))
                                if offering_capacity.lower() == 'q':
                                    _quit = True
                                    break
                                if not offering_capacity:
                                    print("Capacity cannot be empty. Please try again.")
                                    continue
                                offering_capacity = int(offering_capacity)
                                if offering_capacity <= location.get_capacity() and offering_capacity > 0:
                                    print(f"Capacity must be greater than 0 and less than or equal to the location capacity of {location.get_capacity()}. Please try again.")
                                    continue
                                break

                        if _quit == False:
                            try:
                                offering = offerings_catalog.create_offering(location=location, timeslot=timeslot, capacity=offering_capacity, offering_type=offering_type)
                            except ValueError as e:
                                print(f"{e} - The offering was not created and you will be redirected to the main menu")
                                continue
                            print(f"Offering {offering.get_id()} has been successfully created.")
                
                    else:
                        print("\nYou will be redirected back to the admin menu.")
                        continue


            if choice == 3:
                pass

            if choice == 4:
                pass
            
            #! Needs to be tested
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

            #! Needs to be tested
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
                        space_type_input = input("Enter location space type(s) seperated by a comma (e.g., 'rink', 'field', etc.)(or 'q' to quit): ").lower().split(",")
                        if space_type_input == 'q':
                            _quit = True
                            break
                
                        try:
                            location_space_type = [SpaceType(space_type.strip()) for space_type in space_type_input]
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

            #! Needs to be tested - Also needs an input for location_id
            if choice == 10:
                print("\n--------Delete Location--------")
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
            
            #! Needs to be tested
            if choice == 12:
                print("\n--------Get Location based on City and optionally Name and Address--------")
                self.admin_get_location(db)
                
            if choice == 13:
                return