from database import get_session, engine, create_tables
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from catalogs import UsersCatalog, LocationsCatalog, OfferingsCatalog
from models import SpaceType, SpecializationType

def createSampleObjects(db: Session):
    user_catalog = UsersCatalog.get_instance(db)
    
    try:
        new_admin = user_catalog.register_admin("admin", "pass")

        instructor1 = user_catalog.register_instructor("instructor1", "pass", "1234567890", [SpecializationType.hockey, SpecializationType.soccer], ["Montreal", "Laval"])
        instructor2 = user_catalog.register_instructor("instructor2", "pass", "1234567891", [SpecializationType.swim, SpecializationType.yoga], ["Terrebonne", "Laval"])
        instructor3 = user_catalog.register_instructor("instructor3", "pass", "1234567892", [SpecializationType.dance, SpecializationType.soccer], ["Montreal", "Dorval"])

        #client1 = Client(name="Alice Smith", password="password123", phone_number="123-456-7890", is_legal_guardian=False),
        #client2 = Client(name="Bob Johnson", password="securePass456", phone_number="987-654-3210", is_legal_guardian=True, minor_name="Tom Johnson", minor_age=15),
        #client3 = Client(name="Charlie Davis", password="charlie123", phone_number="555-555-5555", is_legal_guardian=True, minor_name="Emily Davis", minor_age=12),
        #client4 = Client(name="Diana Adams", password="dianaSecure", phone_number="444-444-4444", is_legal_guardian=False),

    except ValueError as e:
        print(f"Error creating admin: {str(e)}")

def createLocationsAndOfferings(db: Session):
    from models import Timeslot, OfferingType, SpecializationType
    import datetime
    offerings_catalog = OfferingsCatalog.get_instance(db)
    location_catalog = LocationsCatalog.get_instance(db)
    try:
        location1 = location_catalog.create_location(name="TD Bank", address="1234 Street", capacity=50, city="Montreal", space_type=[SpaceType.rink, SpaceType.field])
        location2 = location_catalog.create_location(name="FB Dungeon", address="5678 Street", capacity=20, city="Laval", space_type=[SpaceType.field, SpaceType.pool])
        location3 = location_catalog.create_location(name="Googleplex", address="91011 Street", capacity=100, city="Terrebonne", space_type=[SpaceType.pool, SpaceType.gym])
        location4 = location_catalog.create_location(name="Amazon", address="121314 Street", capacity=50, city="Dorval", space_type=[SpaceType.studio, SpaceType.gym])


        timeslot1 = Timeslot(start_time=datetime.time(9, 0), end_time=datetime.time(10, 0), day_of_week="Monday",start_date=datetime.date(2024, 10, 16), end_date=datetime.date(2024, 10, 16), schedule_id=location1.get_schedule().get_id())
        timeslot2 = Timeslot(start_time=datetime.time(10, 0), end_time=datetime.time(11, 0), day_of_week="Tuesday",start_date=datetime.date(2024, 10, 17), end_date=datetime.date(2024, 10, 17), schedule_id=location2.get_schedule().get_id())
        timeslot3 = Timeslot(start_time=datetime.time(11, 0), end_time=datetime.time(12, 0), day_of_week="Wednesday",start_date=datetime.date(2024, 10, 18), end_date=datetime.date(2024, 10, 18), schedule_id=location3.get_schedule().get_id())
        timeslot4 = Timeslot(start_time=datetime.time(12, 0), end_time=datetime.time(13, 0), day_of_week="Thursday",start_date=datetime.date(2024, 10, 19), end_date=datetime.date(2024, 10, 19), schedule_id=location4.get_schedule().get_id())

        offering1 = offerings_catalog.create_offering(location=location1, capacity=50, timeslot=timeslot1, offering_type=OfferingType.private, specialization=SpecializationType.hockey)
        offering2 = offerings_catalog.create_offering(location=location2, capacity=20, timeslot=timeslot2, offering_type=OfferingType.group, specialization=SpecializationType.soccer)
        offering3 = offerings_catalog.create_offering(location=location3, capacity=100, timeslot=timeslot3, offering_type=OfferingType.private, specialization=SpecializationType.swim)
        offering4 = offerings_catalog.create_offering(location=location4, capacity=50, timeslot=timeslot4, offering_type=OfferingType.group, specialization=SpecializationType.yoga)


    except ValueError as e:
        print(f"Error creating location: {str(e)}")

    

def main():
    create_tables()
    db: Session = next(get_session())  
    user_catalog = UsersCatalog.get_instance(db)
    location_catalog = LocationsCatalog.get_instance(db)
    inspector = inspect(engine)
    #print("Existing tables:")
    #print(inspector.get_table_names())
    


    print("\n\nWelcome to the Lesson Management System")
    createSampleObjects(db)
    createLocationsAndOfferings(db)
    main_menu_options = """
    Options:
    1. Login
    2. Register as Client
    3. Register as Instructor
    4. Register as Admin
    5. View Offerings (Public)
    6. Exit"""

    while True:

        choice = None
        while True:
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

                if user_type == "instructor":

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
                    if user_phone_number:
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
                    client_menu(client=user, db=db)

                if user.get_type() == "instructor":
                    print(f"\nWelcome {user.get_name()}! You have successfully logged in as an instructor.")
                    user.instructor_menu(db=db)
                
                if user.get_type() == "admin": 
                    print(f"\nWelcome {user.get_name()}! You have successfully logged in as an admin.")
                    user.admin_menu(db)
        
        if choice ==2: #TODO Implement after finishing Client model
            print("\n--------Register as Client--------")
            client_name = str(input("Enter your name: "))
            client_is_underage = str(input("Are you under 18? (yes/no): "))


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
                                break
                    break
            
            if _quit == False:
                while True:
                    instructor_available_cities = str(input("Enter available cities (comma separated) (or 'q' to quit): "))
                    if instructor_available_cities.lower() == 'q':
                        _quit = True
                        print("\nYou will be redirected to the main menu")
                        break
                    if not instructor_available_cities:
                        print("Available cities cannot be empty. Please try again.")
                        continue
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
            if user_catalog.has_admin():
                print("\nAn admin already exists for this organization. You will be redirected to the main menu.")
                continue
            else:
                print("\n--------Register as Admin--------")
                admin_name = None
                admin_password = None
                _quit = False

                while True:
                    admin_name = str(input("Enter your name (or 'q' to quit): "))
                    if admin_name.lower() == 'q':
                        _quit = True
                        print("\nYou will be redirected to the main menu")
                        break
                    if not admin_name:
                        print("Name cannot be empty. Please try again.")
                        continue
                    break
                
                if _quit == False:
                    while True:
                        admin_password = str(input("Enter your password (or 'q' to quit): "))
                        if admin_password.lower() == 'q':
                            _quit = True
                            print("\nYou will be redirected to the main menu")
                            break
                        if not admin_password:
                            print("Password cannot be empty. Please try again.")
                            continue
                        break

                if _quit == False:
                    try:
                        admin = user_catalog.register_admin(admin_name, admin_password)
                    except ValueError as e:
                        print(f"{e} - The account was not created and you will be redirected to the main menu")
                        continue

                    
                    print(f"Welcome {admin.get_name()}! You have successfully registered as an admin.")
                    admin.admin_menu(db)
                
        if choice == 5:#TODO Implement view offerings
            print("\n--------View Offerings--------")
            pass

        if choice == 6:
            print("\nGoodbye!")
            break

    db.close()

if __name__ == "__main__":
    main()
