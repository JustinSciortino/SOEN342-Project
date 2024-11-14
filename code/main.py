from database import get_session, engine, create_tables
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from catalogs import UsersCatalog, LocationsCatalog, OfferingsCatalog, LessonsCatalog, BookingsCatalog
from models import SpaceType, SpecializationType

def createSampleObjects(db: Session):
    from models import Timeslot, LessonType, SpecializationType
    import datetime
    offerings_catalog = OfferingsCatalog.get_instance(db)
    location_catalog = LocationsCatalog.get_instance(db)
    user_catalog = UsersCatalog.get_instance(db)
    lessons_catalog = LessonsCatalog.get_instance(db)
    bookings_catalog = BookingsCatalog.get_instance(db)
    
    try:
        new_admin = user_catalog.register_admin("admin", "pass")

        instructor1 = user_catalog.register_instructor("i1", "pass", "1234567890", [SpecializationType.hockey, SpecializationType.soccer], ["Montreal", "Laval"])
        instructor2 = user_catalog.register_instructor("instructor2", "pass", "1234567891", [SpecializationType.swim, SpecializationType.yoga], ["Terrebonne", "Laval"])
        instructor3 = user_catalog.register_instructor("instructor3", "pass", "1234567892", [SpecializationType.dance, SpecializationType.soccer], ["Montreal", "Dorval"])

        client1 = user_catalog.register_client(name="a", password="pass", phone_number="1234567890")
        client2 = user_catalog.register_client(name="B", password="pass", phone_number="9876543210")
        client3 = user_catalog.register_client(name="c", password="pass", phone_number="5555555555")
        client4 = user_catalog.register_client(name="d", password="pass", phone_number="4444444444")

        minor1 = user_catalog.create_minor(guardian=client1, name="minor1", age=10, relationship_with_guardian="son")
        minor2 = user_catalog.create_minor(guardian=client2, name="minor2", age=12, relationship_with_guardian="daughter")
        minor3 = user_catalog.create_minor(guardian=client2, name="minor3", age=8, relationship_with_guardian="grandchild")

        location1 = location_catalog.create_location(name="TD Bank", address="1234 Street", capacity=50, city="Montreal", space_type=[SpaceType.rink, SpaceType.field])
        location2 = location_catalog.create_location(name="FB Dungeon", address="5678 Street", capacity=20, city="Laval", space_type=[SpaceType.field, SpaceType.pool])
        location3 = location_catalog.create_location(name="Googleplex", address="91011 Street", capacity=100, city="Terrebonne", space_type=[SpaceType.pool, SpaceType.gym])
        location4 = location_catalog.create_location(name="Amazon", address="121314 Street", capacity=50, city="Dorval", space_type=[SpaceType.studio, SpaceType.gym])

        timeslot1 = Timeslot(start_time=datetime.time(9, 0), end_time=datetime.time(10, 0), day_of_week="Monday",start_date=datetime.date(2024, 10, 16), end_date=datetime.date(2024, 10, 16), schedule_id=location1.get_schedule().get_id())
        timeslot2 = Timeslot(start_time=datetime.time(10, 0), end_time=datetime.time(11, 0), day_of_week="Tuesday",start_date=datetime.date(2024, 10, 17), end_date=datetime.date(2024, 10, 17), schedule_id=location2.get_schedule().get_id())
        timeslot3 = Timeslot(start_time=datetime.time(11, 0), end_time=datetime.time(12, 0), day_of_week="Wednesday",start_date=datetime.date(2024, 10, 18), end_date=datetime.date(2024, 10, 18), schedule_id=location3.get_schedule().get_id())
        timeslot4 = Timeslot(start_time=datetime.time(12, 0), end_time=datetime.time(13, 0), day_of_week="Thursday",start_date=datetime.date(2024, 10, 19), end_date=datetime.date(2024, 10, 19), schedule_id=location4.get_schedule().get_id())

        lesson1 = lessons_catalog.create_lesson(capacity=None, location=location1, timeslot=timeslot1, lesson_type=LessonType.private, specialization=SpecializationType.hockey)
        lesson2 = lessons_catalog.create_lesson(capacity=30, location=location2, timeslot=timeslot2, lesson_type=LessonType.group, specialization=SpecializationType.soccer)
        lesson3 = lessons_catalog.create_lesson(capacity=100, location=location3, timeslot=timeslot3, lesson_type=LessonType.private, specialization=SpecializationType.swim)
        lesson4 = lessons_catalog.create_lesson(capacity=50, location=location4, timeslot=timeslot4, lesson_type=LessonType.group, specialization=SpecializationType.yoga)

        offering1 = offerings_catalog.create_offering(lesson=lesson1, instructor=instructor1)
        offering2 = offerings_catalog.create_offering(lesson=lesson2, instructor=instructor2)
        offering3 = offerings_catalog.create_offering(lesson=lesson3, instructor=instructor3)

        booking1 = bookings_catalog.create_booking(client=client1, offering=offering1, minor=minor1)
        booking2 = bookings_catalog.create_booking(client=client2, offering=offering2, minor=minor2)
        booking3 = bookings_catalog.create_booking(client=client2, offering=offering3, minor=minor3)
        booking4 = bookings_catalog.create_booking(client=client3, offering=offering1)
        booking5 = bookings_catalog.create_booking(client=client4, offering=offering2)


    except ValueError as e:
        print()
        #print(f"Error creating admin: {str(e)}")    

def main():
    create_tables()
    db: Session = next(get_session())  
    user_catalog = UsersCatalog.get_instance(db)

    print("\n\nWelcome to the Lesson Management System")
    createSampleObjects(db)
    main_menu_options = """
    Options:
    1. Login
    2. Register as Client
    3. Register as Instructor
    4. View Offerings (Public)
    5. Exit"""

    while True:

        choice = None
        while True:
            print("\n----------Main Menu----------")
            print(main_menu_options)
            choice = input("\nSelect an option: ")
            if choice.strip() == "":
                print("Invalid choice. Please enter a number.")
                continue
            
            try:
                choice = int(choice)
                if choice not in range(1, 7):
                    print("\nInvalid choice. Please enter a number between 1 and 6.")
                    continue
                break
            except ValueError:
                print("\nInvalid choice. Please enter a valid number.")
                continue

        if choice == 1:

            print("\n--------Login--------")
            _quit = False
            while True:
                user_type = str(input("Login as (client/instructor/admin) (or 'q' to quit): "))
                if user_type.lower() == 'q':
                    _quit = True
                    print("\nYou will be redirected to the main menu")
                    break

                if user_type not in ["client", "instructor", "admin"]:
                    print("Invalid user type. Please try again.")
                    continue
                break

            user_name = None
            
            if _quit == False:
                while True:
                    user_name = str(input("Enter your name (or 'q' to quit): "))
                    if user_name.lower() == 'q':
                        _quit = True
                        print("\nYou will be redirected to the main menu")
                        break
                    if not user_name:
                        print("Name cannot be empty. Please try again.")
                        continue
                    break

            user_phone_number = None

            if _quit == False:

                if user_type == "instructor" or user_type == "client":

                    while True:
                        user_phone_number = str(input("Enter your phone number (or 'q' to quit): "))
                        if user_phone_number.lower() == 'q':
                            _quit = True
                            print("\nYou will be redirected to the main menu")
                            break
                        if not user_phone_number:
                            print("Phone number cannot be empty. Please try again.")
                            continue
                        if len(user_phone_number) != 10:
                            print("Phone number must be 10 digits long. Please try again.")
                            continue
                        break

            user_password = None

            if _quit == False:
                while True:
                    user_password = str(input("Enter your password (or 'q' to quit): "))
                    if user_password.lower() == 'q':
                        _quit = True
                        print("\nYou will be redirected to the main menu")
                        break
                    if not user_password:
                        print("Password cannot be empty. Please try again.")
                        continue
                    break

            if _quit == False:
                try:
                    if user_type == "instructor" or user_type == "client":
                        user = user_catalog.login(user_name, user_password, user_phone_number)
                    else:
                        user = user_catalog.login(user_name, user_password)

                except ValueError as e:
                    print(f"{e} - You will be redirected to the main menu")
                    continue

                if user is None:
                    print("\nInvalid credentials. Please try again.")
                    continue

                if user.get_type() == "client":
                    print(f"\nWelcome {user.get_name()}! You have successfully logged in as a client.")
                    user.client_menu(db=db)

                if user.get_type() == "instructor":
                    print(f"\nWelcome {user.get_name()}! You have successfully logged in as an instructor.")
                    user.instructor_menu(db=db)
                
                if user.get_type() == "admin": 
                    print(f"\nWelcome {user.get_name()}! You have successfully logged in as an admin.")
                    user.admin_menu(db)
     
        if choice == 2:
            print("\n--------Register as Client--------")
            
            _quit = False
            client_name = None
            client_phone_number = None
            client_password = None
            minor_name = None
            minor_age = None
            guardian_client_id = None
            new_client = None

            while True:
                client_name = str(input("Enter your name (or 'q' to quit): "))
                if client_name.lower() == 'q':
                    _quit = True
                    print("\nYou will be redirected to the main menu.")
                    break
                if not client_name:
                    print("Name cannot be empty. Please try again.")
                    continue
                break
            
            if _quit == False: 
                client_is_minor = str(input("Are you under 18? (yes/no): ")).lower()

                if client_is_minor == 'yes':
                    guardian_option = str(input("Do you want to (1) create a new legal guardian, or (2) link to an existing guardian? (enter 1 or 2): "))

                    if guardian_option == '1':
                        legal_guardian_name = str(input("Enter the legal guardian's name: "))
                        while True:
                            legal_guardian_phone = str(input("Enter your phone number (or 'q' to quit): "))
                            if legal_guardian_phone.lower() == 'q':
                                _quit = True
                                print("\nYou will be redirected to the main menu.")
                                break
                            if len(legal_guardian_phone) != 10:
                                print("Phone number must be 10 digits long. Please try again.")
                                continue
                            break

                        while True:
                            legal_guardian_password = str(input("Enter your password (or 'q' to quit): "))
                            if legal_guardian_password.lower() == 'q':
                                _quit = True
                                print("\nYou will be redirected to the main menu.")
                                break
                            if not legal_guardian_password:
                                print("Password cannot be empty. Please try again.")
                                continue
                            break

                        

                        while True:
                            relationship_with_guardian = str(input("Enter your relationship with the guardian (ex: son, daughter...): "))
                            if relationship_with_guardian.lower() == 'q':
                                _quit = True
                                print("\nYou will be redirected to the main menu.")
                                break
                            if not relationship_with_guardian:
                                print("Relationship cannot be empty. Please try again.")
                                continue
                            break

                        minor_name = client_name

                        while True:
                            minor_age = int(input(f"{minor_name}, enter your age: "))
                            if not minor_age or minor_age < 1 or minor_age >= 18:
                                print("Age cannot be empty, less than 1, or larger than and including 18. Please try again.")
                                continue
                            break

                        try:
                            existing_guardian = user_catalog.register_client(legal_guardian_name, legal_guardian_phone, legal_guardian_password)
                            print(f"\nLegal Guardian Client, {legal_guardian_name}, has been created.")

                        except ValueError as e:
                            print(f"Error registering legal guardian: {e}")
                            break

                        user_catalog.create_minor(guardian=existing_guardian, name=minor_name, age=minor_age, relationship_with_guardian=relationship_with_guardian)
                        existing_guardian.client_menu(db)
                        print(f"Minor, {minor_name}, has been created.")

                    elif guardian_option == '2':
                        
                        while True:
                            guardian_client_id = int(input("Enter the ID of the existing guardian: "))
                            if not guardian_client_id:
                                print("Client id cannot be empty. Please try again.")
                                continue
                            
                            existing_guardian = user_catalog.get_client_by_id(guardian_client_id)

                            if existing_guardian is None:
                                print("Client does not exist. Please try again.")
                                continue

                            break

                        while True:
                            relationship_with_guardian = str(input("Enter your relationship with the guardian (ex: son, daughter...): "))
                            if relationship_with_guardian.lower() == 'q':
                                _quit = True
                                print("\nYou will be redirected to the main menu.")
                                break
                            if not relationship_with_guardian:
                                print("Relationship cannot be empty. Please try again.")
                                continue
                            break

                        minor_name = client_name
                        
                        while True:
                            minor_age = int(input(f"{minor_name}, enter your age: "))
                            if (not minor_age) or minor_age < 1 or minor_age >= 18:
                                print("Age cannot be empty, less than 1, or larger than and including 18. Please try again.")
                                continue
                            break

                        user_catalog.create_minor(guardian=existing_guardian, name=minor_name, age=minor_age, relationship_with_guardian=relationship_with_guardian)
                        existing_guardian.client_menu(db)
                        print(f"Minor, {minor_name}, has been created and has successfully been linked to the guardian.")

                elif client_is_minor == 'no':
                   
                    while True:
                        client_phone_number = str(input("Enter your phone number (or 'q' to quit): "))
                        if client_phone_number.lower() == 'q':
                            _quit = True
                            print("\nYou will be redirected to the main menu.")
                            break
                        if len(client_phone_number) != 10:
                            print("Phone number must be 10 digits long. Please try again.")
                            continue
                        break

                    while True:
                        client_password = str(input("Enter your password (or 'q' to quit): "))
                        if client_password.lower() == 'q':
                            _quit = True
                            print("\nYou will be redirected to the main menu.")
                            break
                        if not client_password:
                            print("Password cannot be empty. Please try again.")
                            continue
                        break

                    if _quit == False:
                        try:
                            client = user_catalog.register_client(client_name, client_phone_number, client_password)
                            
                        except ValueError as e:
                            print(f"Error registering client: {e}. Please try again.")
                            continue
                        
                        print(f"Welcome {client_name}! You have successfully registered as an client.")
                        client.client_menu(db)
                        

        if choice == 3: 
            from models import SpecializationType
            print("\n--------Register as Instructor--------")
            instructor_name = None
            instructor_phone_number = None
            instructor_specialization = None
            instructor_available_cities = None
            password = None
            valid_specializations = []
            _quit = False

            while True:
                instructor_name = str(input("Enter your name (or 'q' to quit): "))
                if instructor_name.lower() == 'q':
                    _quit = True
                    print("\nYou will be redirected to the main menu")
                    break
                if not instructor_name:
                    print("Name cannot be empty. Please try again.")
                    continue
                break
            
            if _quit == False:
                while True:
                    instructor_phone_number = str(input("Enter your phone number (or 'q' to quit): "))
                    if instructor_phone_number.lower() == 'q':
                        _quit = True
                        print("\nYou will be redirected to the main menu")
                        break
                    if len(instructor_phone_number) != 10:
                        print("Phone number must be 10 digits long. Please try again.")
                        continue
                    break


            if _quit == False:
                while True:
                    password = str(input("Enter your password (or 'q' to quit): "))
                    if password.lower() == 'q':
                        _quit = True
                        print("\nYou will be redirected to the main menu")
                        break
                    if not password:
                        print("Password cannot be empty. Please try again.")
                        continue
                    break
            
            if _quit == False: 
                while True:
                    is_valid = True
                    print(f"Available specialization types: {[spec.value for spec in SpecializationType]}")
                    instructor_specialization = input("Enter instructor specialization as a list seperated by commas (or 'q' to quit): ")
                    if instructor_specialization.lower() == 'q':
                        _quit = True
                        print("\nYou will be redirected to the main menu")
                        break
                    if _quit == False and instructor_specialization:
                        specialization_list = [spec.strip().lower() for spec in instructor_specialization.split(",")]

                        for spec in specialization_list:
                            try:
                                valid_specializations.append(SpecializationType(spec))
                            except ValueError:
                                print(f"'{spec}' is not a valid specialization type. Please try again.")
                                is_valid = False
                                break
                    if is_valid:
                        break

            
            if _quit == False:
                while True:
                    instructor_available_cities = str(input("Enter available cities (comma separated), (or 'q' to quit): "))
                    if instructor_available_cities.lower() == 'q':
                        _quit = True
                        print("\nYou will be redirected to the main menu")
                        break
                    if not instructor_available_cities:
                        print("Available cities cannot be empty. Please try again.")
                        continue
                    instructor_available_cities = ', '.join(city.strip().title() for city in instructor_available_cities.split(","))
                    break

            if _quit == False:
                try:
                    instructor = user_catalog.register_instructor(instructor_name, password, instructor_phone_number, valid_specializations, instructor_available_cities.split(","))
                except ValueError as e:
                    print(f"{e} - The account was not created and you will be redirected to the main menu")
                    continue

                
                print(f"Welcome {instructor.get_name()}! You have successfully registered as an instructor.")
                instructor.instructor_menu(db)

        
        if choice == 4:
            print("\n--------View Offerings (Public)--------")
            
            offerings_catalog = OfferingsCatalog.get_instance(db)

            #TODO refactor
            offerings_with_instructor = offerings_catalog.get_offerings_with_instructor()

            if not offerings_with_instructor:
                print("No offerings available at this time.")
            else:
                print("\nAvailable Offerings:")
                for offering in offerings_with_instructor:
                    print(offering.repr_client())  

        if choice == 5:
            print("\nGoodbye!\n")
            break

    db.close()

if __name__ == "__main__":
    main()