from database import get_session, engine, create_tables
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from catalogs import UsersCatalog

def createSampleObjects(db: Session):
    user_catalog = UsersCatalog.get_instance(db)
    try:
        new_admin = user_catalog.register_admin("admin", "pass")
        #print(new_admin)
        new_instructor = user_catalog.register_instructor("instructor", "pass", "1234567890", ["Math", "Science"], ["Toronto", "Vancouver"])
        #print(new_instructor)
    except ValueError as e:
        print(f"Error creating admin: {str(e)}")

def main():
    create_tables()
    db: Session = next(get_session())  
    user_catalog = UsersCatalog.get_instance(db)
    inspector = inspect(engine)
    print("Existing tables:")
    print(inspector.get_table_names())
    


    print("Welcome to the Lesson Management System")
    #createSampleObjects(db)
    main_menu_options = """
    Options:
    1. Login
    2. Register as Client
    3. Register as Instructor
    4. Register as Admin
    5. View Offerings (Public)
    6. Exit"""

    while True:
        print(main_menu_options)
        choice = int(input("\nSelect an option: "))

        if choice == 1:

            print("\n--------Login--------")
            user_type = str(input("Login as (client/instructor/admin): "))

            if user_type not in ["client", "instructor", "admin"]:
                print("Invalid user type. Please try again.")
                continue

            user_name = None
            
            while True:
                user_name = str(input("Enter your name: "))
                if not user_name:
                    print("Name cannot be empty. Please try again.")
                    continue
                break

            user_phone_number = None

            if user_type == "instructor":

                while True:
                    user_phone_number = str(input("Enter your phone number: "))
                    if not user_phone_number:
                        print("Phone number cannot be empty. Please try again.")
                        continue
                    if len(user_phone_number) != 10:
                        print("Phone number must be 10 digits long. Please try again.")
                        continue
                    break

            user_password = None

            while True:
                user_password = str(input("Enter your password: "))
                if not user_password:
                    print("Password cannot be empty. Please try again.")
                    continue
                break

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
                instructor_menu(instructor=user, db=db)
            
            if user.get_type() == "admin": 
                print(f"\nWelcome {user.get_name()}! You have successfully logged in as an admin.")
                admin_menu(admin=user, db=db)
        
        if choice ==2: #TODO Implement after finishing Client model
            print("\n--------Register as Client--------")
            client_name = str(input("Enter your name: "))
            client_is_underage = str(input("Are you under 18? (yes/no): "))

        if choice == 3: 
            print("\n--------Register as Instructor--------")
            instructor_name = None
            instructor_phone_number = None
            instructor_specialization = None
            instructor_available_cities = None

            while True:
                instructor_name = str(input("Enter your name: "))
                if not instructor_name:
                    print("Name cannot be empty. Please try again.")
                    continue
                break

            while True:
                instructor_phone_number = str(input("Enter your phone number: "))
                if len(instructor_phone_number) != 10:
                    print("Phone number must be 10 digits long. Please try again.")
                    continue
                break

            while True:
                instructor_specialization = str(input("Enter your specialization: "))
                if not instructor_specialization:
                    print("Specialization cannot be empty. Please try again.")
                    continue
                break

            while True:
                instructor_available_cities = str(input("Enter available cities (comma separated): "))
                if not instructor_available_cities:
                    print("Available cities cannot be empty. Please try again.")
                    continue
                break
            try:
                instructor = user_catalog.register_instructor(instructor_name, "pass", instructor_phone_number, instructor_specialization.split(","), instructor_available_cities.split(","))
            except ValueError as e:
                print(f"{e} - The account was not created and you will be redirected to the main menu")
                continue

            
            print(f"Welcome {instructor.get_name()}! You have successfully registered as an instructor.")
            instructor_menu(instructor, db)

        if choice == 4: 
            if user_catalog.has_admin():
                print("\nAn admin already exists for this organization. You will be redirected to the main menu.")
                continue
            else:
                print("\n--------Register as Admin--------")
                admin_name = None
                admin_password = None

                while True:
                    admin_name = str(input("Enter your name: "))
                    if not admin_name:
                        print("Name cannot be empty. Please try again.")
                        continue
                    break

                while True:
                    admin_password = str(input("Enter your password: "))
                    if not admin_password:
                        print("Password cannot be empty. Please try again.")
                        continue
                    break
                try:
                    admin = user_catalog.register_admin(admin_name, admin_password)
                except ValueError as e:
                    print(f"{e} - The account was not created and you will be redirected to the main menu")
                    continue

                
                print(f"Welcome {admin.get_name()}! You have successfully registered as an admin.")
                admin_menu(admin, db)
                

        if choice == 5:
            print("\n--------View Offerings--------")
            #TODO Implement view offerings
            pass

        if choice == 6:
            print("\nGoodbye!")
            break

    db.close()


def client_menu(client, db):
    pass #TODO Add update account functionality 
def admin_menu(admin, db):
    pass
def instructor_menu(instructor, db):
    pass


    """ while True:
        print("\nOptions:")
        print("1. Login")
        print("2. Register as Client")
        print("3. Register as Instructor")
        print("4. View Offerings (Public)")
        print("5. Exit")
        
        choice = input("Select an option: ")

        if choice == '1':
            user_type = input("Login as (client/instructor/admin): ")
            
            if user_type == "client":
                client_id = input("Enter your client ID: ")
                try:
                    client_id = int(client_id)  # Ensure client ID is an integer
                    client = login_client(client_id, db)  # Call the login function with the inputted ID
                    if client:
                        client_menu(client_id, db)
                    else:
                        print("Invalid client ID.")
                except ValueError:
                    print("Client ID must be a valid number.")

            elif user_type == "instructor":
                instructor_id = input("Enter your instructor ID: ")
                try:
                    instructor_id = int(instructor_id)  # Ensure instructor ID is an integer
                    instructor = login_instructor(instructor_id, db)  # Call the login function with the inputted ID
                    if instructor:
                        instructor_menu(instructor_id, db)
                    else:
                        print("Invalid instructor ID.")
                except ValueError:
                    print("Instructor ID must be a valid number.")

            elif user_type == "admin":
                admin_id = input("Enter your admin ID: ")
                try:
                    admin_id = int(admin_id)  # Ensure admin ID is an integer
                    admin = login_admin(admin_id, db)  # Call the login function with the inputted ID
                    if admin:
                        admin_menu(admin_id, db)
                    else:
                        print("Invalid admin ID.")
                except ValueError:
                    print("Admin ID must be a valid number.")

        elif choice == '2':
            # Sign up as client
            name = input("Enter your name: ")
            phone_number = input("Enter your phone number: ")
            email = input("Enter your email: ")
            is_underage = input("Are you under 18? (yes/no): ").strip().lower()
            guardian_id = None
            if is_underage == "yes":
                guardian_id = input("Enter guardian ID: ")
            signup_client_process(name, phone_number, email, is_underage == "yes", guardian_id, db)

        elif choice == '3':
            # Sign up as instructor
            name = input("Enter your name: ")
            phone_number = input("Enter your phone number: ")
            email = input("Enter your email: ")
            specialization = input("Enter your specialization: ")
            available_cities = input("Enter available cities (comma separated): ").split(",")
            signup_instructor_process(name, phone_number, email, specialization, available_cities, db)

        elif choice == '4':
            # View public offerings
            offerings = view_offerings(db)
            if offerings:
                for offering in offerings:
                    print(offering)
            else:
                print("No offerings available.")

        elif choice == '5':
            print("Goodbye!")
            break

    db.close()  # Close the session

# Client Menu
def client_menu(client_id, db):
    while True:
        print("\nClient Options:")
        print("1. View Offerings")
        print("2. Book Offering")
        print("3. View Bookings")
        print("4. Cancel Booking")
        print("5. Logout")

        choice = input("Select an option: ")
        if choice == '1':
            offerings = view_offerings(db)
            if offerings:
                for offering in offerings:
                    print(offering)

        elif choice == '2':
            offering_id = input("Enter Offering ID to book: ")
            book_offering(client_id, offering_id, db)

        elif choice == '3':
            bookings = view_client_bookings(client_id, db)
            if bookings:
                for booking in bookings:
                    print(booking)

        elif choice == '4':
            booking_id = input("Enter Booking ID to cancel: ")
            cancel_booking(client_id, booking_id, db)

        elif choice == '5':
            break

# Instructor Menu
def instructor_menu(instructor_id, db):
    while True:
        print("\nInstructor Options:")
        print("1. View Offerings")
        print("2. Teach Offering")
        print("3. Logout")

        choice = input("Select an option: ")
        if choice == '1':
            offerings = view_instructor_offerings(instructor_id, db)
            if offerings:
                for offering in offerings:
                    print(offering)

        elif choice == '2':
            offering_id = input("Enter Offering ID to teach: ")
            teach_offering(instructor_id, offering_id, db)

        elif choice == '3':
            break

# Admin Menu
def admin_menu(admin_id, db):
    while True:
        print("\nAdmin Options:")
        print("1. View Offerings")
        print("2. Create Offering")
        print("3. Delete Client/Instructor Account")
        print("4. View Client Bookings")
        print("5. Modify Offering")
        print("6. Cancel Offering")
        print("7. Logout")

        choice = input("Select an option: ")
        if choice == '1':
            offerings = view_offerings(db)
            if offerings:
                for offering in offerings:
                    print(offering)

        elif choice == '2':
            location = input("Enter location: ")
            lesson_type = input("Enter lesson type: ")
            start_time = input("Enter start time: ")
            end_time = input("Enter end time: ")
            instructor_id = input("Enter instructor ID: ")
            create_offering(location, lesson_type, start_time, end_time, instructor_id, db)

        elif choice == '3':
            account_id = input("Enter Account ID to delete: ")
            delete_account(account_id, db)

        elif choice == '4':
            bookings = view_client_bookings_by_admin(db)
            if bookings:
                for booking in bookings:
                    print(booking)

        elif choice == '5':
            offering_id = input("Enter Offering ID to modify: ")
            modify_offering(offering_id, db)

        elif choice == '6':
            offering_id = input("Enter Offering ID to cancel: ")
            cancel_offering(offering_id, db)

        elif choice == '7':
            break """

if __name__ == "__main__":
    main()
