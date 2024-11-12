from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column, Session
from database.config import Base
from models import User
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
    
    def admin_menu(self, db: Session):
        from catalogs import UsersCatalog, LocationsCatalog, OfferingsCatalog, BookingsCatalog, LessonsCatalog
        locations_catalog = LocationsCatalog.get_instance(db)
        users_catalog = UsersCatalog.get_instance(db)  
        offerings_catalog = OfferingsCatalog.get_instance(db)
        bookings_catalog = BookingsCatalog.get_instance(db)
        lessons_catalog = LessonsCatalog.get_instance(db)

        admin_menu_options = """
        Admin Options:
        1. View Offerings
        2. View Lessons
        3. Create Lesson
        4. Cancel Offering or Lesson 
        5. Delete Client/Instructor Account
        6. View Client Bookings (Optionally Cancel Client Booking)
        7. Add Location
        8. View Location Schedule
        9. Get All Locations
        10. Get Location from ID or City (and optionally Name and Address)
        11. Logout and return to main menu"""

        #* For cancel offering and lesson, delete the corresponding 

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

                    if choice not in range(1, 12):
                        print("\nInvalid choice. Please enter a number between 1 and 11.")

                        continue
                    break
                except ValueError:
                    print("\nInvalid choice. Please enter a valid number.")
                    continue


            if choice == 1:
                print("\n--------View Offerings--------")
                offering_city = None
                offering_specialization = None
                offering_type = None
                _quit = False


                offering_city = input("Enter offering city (or 'q' to quit or click 'enter' to not add a city): ").strip() or None
                if offering_city is not None and offering_city.lower() == 'q':
                    _quit = True

                if _quit == False:

                    from models import SpecializationType
                    print(f"Available specialization types: {[spec.value for spec in SpecializationType]}")
                    offering_specialization = input("Enter offering specialization (or 'q' to quit or 'enter' to not add a specialization): ").strip() or None
                    if offering_specialization is not None and offering_specialization.lower() == 'q':
                        _quit = True

                    if _quit == False and offering_specialization:
                        offering_specialization = SpecializationType(offering_specialization)
                
                if _quit == False:
                    from models import LessonType
                    print(f"Available offering types: {[offering_type.value for offering_type in LessonType]}")
                    offering_type = input("Enter offering type (or 'q' to quit or 'enter' to not add an offering type): ").strip() or None
                    if offering_type is not None and offering_type.lower() == 'q':
                        _quit = True

                if _quit == False:

                    offerings = offerings_catalog.admin_get_all_offerings(city=offering_city, specialization=offering_specialization, _type=offering_type)


                    if not offerings:
                        print("\nNo offerings found.")

                    for offering in offerings:
                        print(offering.repr_admin())

                else:
                    print("\nYou will be redirected back to the admin menu.")
                    continue

            if choice == 2:
                lesson_city = None
                lesson_specialization = None
                lesson_type = None
                _quit = False


                lesson_city = input("Enter lesson city (or 'q' to quit or click 'enter' to not add a city): ").strip() or None
                if lesson_city is not None and lesson_city.lower() == 'q':
                    _quit = True

                if _quit == False:

                    from models import SpecializationType
                    print(f"Available specialization types: {[spec.value for spec in SpecializationType]}")
                    lesson_specialization = input("Enter lesson specialization ()(or 'q' to quit or 'enter' to not add a specialization): ").strip() or None
                    if lesson_specialization is not None and lesson_specialization.lower() == 'q':
                        _quit = True
                    if _quit == False and lesson_specialization:
                        lesson_specialization = SpecializationType(lesson_specialization)
                
                if _quit == False:
                    from models import LessonType
                    print(f"Available offering types: {[lesson_type.value for lesson_type in LessonType]}")
                    lesson_type = input("Enter lesson type (or 'q' to quit or 'enter' to not add an offering type): ").strip() or None
                    if lesson_type is not None and lesson_type.lower() == 'q':
                        _quit = True

                if _quit == False:

                    lessons = lessons_catalog.admin_get_all_lessons(city=lesson_city, specialization=lesson_specialization, _type=lesson_type)


                    if not lessons:
                        print("\nNo offerings found.")

                    for lesson in lessons:
                        print(lesson.repr_admin())

                else:
                    print("\nYou will be redirected back to the admin menu.")
                    continue

            if choice == 3:
                print("\n--------Create Lesson--------")
                location_id = None
                _quit=False

                available_locations = locations_catalog.get_all_locations()

                if not available_locations:
                    print("No locations found. Please add a location before creating a lesson.")
                    continue
                else:
                    print("\n","Available locations:")
                    for location in available_locations:
                        print(location)

                while True:
                    location_id = str(input("\nEnter location id from one of locations above (or 'q' to quit): "))
                    if location_id.lower() == 'q':
                        _quit = True
                        break
                    if not location_id:
                        print("Id cannot be empty. Please try again.")
                        continue
                    if not location_id.isdigit():
                        print("Id must be a number. Please try again.")
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
                        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                        day_of_week = str(input("Enter day of the week (e.g., 'Monday', 'Tuesday', etc.)(or 'q' to quit): "))
                        if day_of_week.lower() == 'q':
                            _quit = True
                            break
                        if not day_of_week:
                            print("Day of the week cannot be empty. Please try again.")
                            continue

                        if day_of_week not in days:
                            print("Invalid day of the week. Please enter a valid day.")
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
                                today = datetime.date.today()
                                if start_date < today:
                                    print("Start date must be after today's date. Please try again.")
                                    continue

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
                                today = datetime.date.today()
                                if end_date < today:
                                    print("End date must be after today's date. Please try again.")
                                    continue
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
                            print("Timeslot conflicts with existing timeslots. Lesson cannot be created.")
                            continue

                        lesson_type = None
                        lesson_capacity = None
                        specialization = None

                        while True:
                            from models import LessonType
                            valid_lesson_types = [lesson_type.value.lower() for lesson_type in LessonType]
                            print(f"Available lesson types: {valid_lesson_types}")
                            lesson_type_input = input("Enter lesson type (e.g. private or group)(or 'q' to quit): ").lower()
                            if lesson_type_input == 'q':
                                _quit = True
                                break

                            if not lesson_type_input:
                                print("Lesson type cannot be empty. Please try again.")
                                continue

                            if lesson_type_input not in valid_lesson_types:
                                print(f"Invalid lesson type. Please enter one of: {', '.join(valid_lesson_types)}")
                                continue

                            lesson_type = LessonType(lesson_type_input)
                            break


                        if _quit == False:
                            from models import SpecializationType, SPACE_SPECIALIZATION_MAP, SpaceType
                            while True:

                                available_specs = set()
                                for space_type in location.get_space_type():
                                    space_type_enum = SpaceType(space_type)
                                    available_specs.update(SPACE_SPECIALIZATION_MAP[space_type_enum])
                                
                                print(f"Available specializations: {[spec.value for spec in available_specs]}")
                                specialization_input = input("Enter lesson specialization (or 'q' to quit): ").strip().lower()
                                
                                if specialization_input == 'q':
                                    _quit = True
                                    break
                                
                                if not specialization_input:
                                    print("Specialization cannot be empty. Please try again.")
                                    continue
                                
                                try:
                                    specialization = SpecializationType(specialization_input)
                                    if specialization not in available_specs:
                                        print(f"Invalid specialization for the given space type(s). Please choose from the available options.")
                                        continue
                                    break
                                except ValueError:
                                    print(f"Invalid specialization. Please enter one of: {', '.join([spec.value for spec in available_specs])}")
                                    continue


                        if _quit == False and lesson_type == LessonType.group:
                            while True:
                                lesson_capacity = str(input("Enter lesson capacity (or 'q' to quit): "))
                                if lesson_capacity.lower() == 'q':
                                    _quit = True
                                    break
                                if not lesson_capacity:
                                    print("Capacity cannot be empty. Please try again.")
                                    continue
                                lesson_capacity = int(lesson_capacity)
                                if lesson_capacity > location.get_capacity() or lesson_capacity <= 0:
                                    print(f"Capacity must be greater than 0 and less than or equal to the location capacity of {location.get_capacity()}. Please try again.")
                                    continue
                                break

                        if _quit == False:
                            try:
                                lesson = lessons_catalog.create_lesson(location=location, timeslot=timeslot, capacity=lesson_capacity, lesson_type=lesson_type, specialization=specialization)
                                locations_catalog.add_timeslot(location, timeslot)
                                
                            except ValueError as e:
                                print(f"{e} - The lesson was not created and you will be redirected to the main menu")
                                continue
                            print(f"Lesson {lesson.get_id()} has been successfully created.")
                
                    else:
                        print("\nYou will be redirected back to the admin menu.")
                        continue
            
            if choice == 4:
                print("\n--------Cancel Offering or Lesson--------")
                cancel_choice = None
                option_str = """
                Do you want to cancel an offering or delete a lesson? Enter offering or lesson (or 'q' to quit) 
                (Note that if an offering is cancelled, the associated lesson will not be deleted. If a lesson is deleted, the associated offering will be deleted and cancelled): """
                while True:
                    cancel_choice = input(option_str).strip().lower()
                    if cancel_choice == 'q':
                        break
                    if cancel_choice not in ['offering', 'lesson']:
                        print("Invalid choice. Please enter 'offering' or 'lesson'.")
                        continue
                    break
                if cancel_choice == 'offering':
                    offering_id = None
                    offering = None
                    _quit = False

                    while True:
                        offering_id = str(input("Enter offering ID (or 'q' to quit): "))
                        if offering_id.lower() == 'q':
                            _quit = True
                            break
                        if not offering_id:
                            print("Id cannot be empty. Please try again.")
                            continue
                        if not offering_id.isdigit():
                            print("Id must be a number. Please try again.")
                            continue
                        break

                    if _quit == False:
                        offering_id = int(offering_id)
                        try:
                            offering = offerings_catalog.get_offering_by_id(offering_id)
                            offerings_catalog.delete_offering(offering=offering)
                            print(f"Offering {offering.get_id()} has been successfully cancelled.")
                        except ValueError as e:
                            print(f"\n{e} - The offering was not found.")
                            continue
                    else:
                        print("\nYou will be redirected back to the admin menu.")
                        continue

                if cancel_choice == "lesson":
                    lesson_id = None
                    lesson = None
                    _quit = False

                    while True:
                        lesson_id = str(input("Enter lesson ID (or 'q' to quit): "))
                        if lesson_id.lower() == 'q':
                            _quit = True
                            break
                        if not lesson_id:
                            print("Id cannot be empty. Please try again.")
                            continue
                        if not lesson_id.isdigit():
                            print("Id must be a number. Please try again.")
                            continue
                        break

                    if _quit == False:
                        lesson_id = int(lesson_id)
                        try:
                            lesson = lessons_catalog.get_lesson_by_id(lesson_id)
                            lesson_offering = lesson.get_offerings()
                            if lesson_offering:
                                offerings_catalog.delete_offering(lesson_offering)
                                print(f"Associated offering has been successfully cancelled.")
                            lessons_catalog.cancel_lesson(lesson)
                            print(f"Lesson {lesson_id} has been successfully cancelled.")
                        except ValueError as e:
                            print(f"\n{e} - The lesson was not found.")
                            continue
                    else:
                        print("\nYou will be redirected back to the admin menu.")
                        continue
            
            
            if choice == 5:
                print("\n--------Delete Client/Instructor Account--------")
                account_name = None
                account_id = None
                _quit = False

                while True:
                    account_name = str(input("Enter the name or ID of the account to delete (or 'q' to quit): "))
                    if account_name.lower() == 'q':
                        _quit = True
                        break
                    if not account_name:
                        print("Name cannot be empty. Please try again.")
                        continue
                    if account_name.isdigit():
                        account_id = int(account_name)
                    break

                if _quit == False:
                    try:
                        users_catalog.delete_user(account_name, account_id)
                    except ValueError as e:
                        print(f"{e} - The account was not deleted and you will be redirected to the main menu")
                        continue
                    print(f"Account {account_name} has been successfully deleted.")
                else:
                    print("\nYou will be redirected back to the admin menu.")
            
            if choice == 6:
                print("\n--------View Client Bookings (Optionally Cancel Client Booking)--------")
                client_id = None
                client_name = None
                _quit = False
                client = None

                while True:
                    client_name = str(input("Enter client name or ID (or 'q' to quit): "))
                    if client_name.lower() == 'q':
                        _quit = True
                        break
                    if not client_name:
                        print("Name cannot be empty. Please try again.")
                        continue
                    if client_name.isdigit():
                        client_id = int(client_name)
                    break

                if _quit == False:
                    try:
                        if client_id:
                            client = users_catalog.get_user_by_id(client_id)
                            if client.get_type() != "client":
                                raise ValueError("The account is not a client.")
                        else:
                            client = users_catalog.get_user(client_name)
                            if client.get_type() != "client":
                                raise ValueError("The account is not a client.")
                    except ValueError as e:
                        print(f"{e} - The client was not found.")
                        continue

                    client_bookings = client.get_bookings()

                    if not client_bookings:
                        print(f"\nClient {client.get_name()} has no bookings.")
                        continue

                    print(f"\nClient {client.get_name()} bookings:")
                    for booking in client_bookings:
                        if booking.get_minor_id():
                            print(booking.repr_minor())
                        else:
                            print(booking.repr_client())
                        

                    cancel_booking_id = None

                    while True:
                        cancel_booking_resp = str(input("Would you like to cancel a booking? (y/n): "))
                        if cancel_booking_resp.lower() == 'n':
                            break
                        if not cancel_booking_resp:
                            print("Response cannot be empty. Please try again.")
                            continue
                        if cancel_booking_resp.lower() != 'y' and cancel_booking_resp.lower() != 'n':
                            print("Invalid response. Please enter 'y' or 'n'.")
                            continue
                        if cancel_booking_resp.lower() == 'y':
                            while True:
                                cancel_booking_id = str(input("Enter booking ID to cancel (or 'q' to quit): "))
                                if cancel_booking_id.lower() == 'q':
                                    _quit = True
                                    break
                                if not cancel_booking_id:
                                    print("Id cannot be empty. Please try again.")
                                    continue
                                if not cancel_booking_id.isdigit():
                                    print("Id must be a number. Please try again.")
                                    continue
                                break
                            if _quit == False:
                                cancel_booking_id = int(cancel_booking_id)
                                try:
                                    bookings_catalog.cancel_booking_(cancel_booking_id)
                                    print(f"Booking {cancel_booking_id} has been successfully cancelled.")
                                    break
                                except ValueError as e:
                                    print(f"{e} - The booking was not found.")
                                    continue
                                break
                            else:
                                print("\nYou will be redirected back to the admin menu.")
                                break
                        
                else:
                    print("\nYou will be redirected back to the admin menu.")
                    continue

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
                        from models import SpaceType
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
                print("\n--------View Location Schedule--------")
                location_id = None
                location = None
                _quit = False

                while True:
                    location_id = str(input("Enter location ID (or 'q' to quit): "))
                    if location_id.lower() == 'q':
                        _quit = True
                        break
                    if not location_id:
                        print("Id cannot be empty. Please try again.")
                        continue
                    if not location_id.isdigit():
                        print("Id must be a number. Please try again.")
                        continue
                    break

                if _quit == False:
                    location_id = int(location_id)
                    try:
                        location = locations_catalog.get_location_by_id(location_id)
                    except ValueError as e:
                        print(f"\n{e} - The location was not found.")
                        continue

                if location and _quit == False:
                    timeslots = location.get_schedule().get_timeslots()
                    print(f"\nLocation {location.get_name()} schedule:")
                    if not timeslots:
                        print("\nNo timeslots yet in the location schedule.")
                    else:
                        for timeslot in timeslots:
                            print(timeslot)
                else:
                    print("\nYou will be redirected back to the admin menu.")
                    continue

            if choice == 9:
                print("\n--------Get All Locations--------")
                locations = locations_catalog.get_all_locations()
                if not locations:
                    print("\nNo locations found.")
                for location in locations:
                    print(location)
            
            if choice == 10:
                print("\n--------Get Location from ID or City (and optionally Name and Address)--------")
                location_city = None
                location_name = None
                location_address = None
                location_id = None
                _quit = False

                while True:
                    location_city = str(input("Enter location city or ID (or 'q' to quit): "))
                    if location_city.lower() == 'q':
                        _quit = True
                        break
                    if not location_city:
                        print("City cannot be empty. Please try again.")
                        continue
                    if location_city.isdigit():
                        location_id = int(location_city)
                        break
                    break
                
                if _quit == False and not location_id:
                    location_name = str(input("Enter location name (optional - click Enter to not add a name)(or 'q' to quit): "))
                    if location_name.lower() == 'q':
                        _quit = True

                if _quit == False and not location_id:
                    location_address = str(input("Enter location address (optional - click Enter to not add an address)(or 'q' to quit): "))
                    if location_address.lower() == 'q':
                        _quit = True
                
                if _quit == False:
                    if location_name and location_address:
                        try:
                            location = locations_catalog.get_location(city=location_city, name=location_name, address=location_address)
                            print(location)
                        except ValueError as e:
                            print(f"{e} - The location was not found.")
                            break  
                    else:
                        try:
                            if location_id:
                                location = locations_catalog.get_location_by_id(location_id)
                                print('\n',location)
                            else:
                                location = locations_catalog.get_location(city=location_city)
                                for l in location:
                                    print('\n',l)
                        except ValueError as e:
                            print(f"{e} - The location was not found.")
                            break
                else:
                    print("\nYou will be redirected back to the admin menu.")
                
            if choice == 11:
                print(f"\nLogging out as admin and returning to the main menu. Goodbye {self.name}!")
                return