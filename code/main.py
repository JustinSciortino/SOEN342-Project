from db.config import get_db
from logic.logic import *

def main():
    db: Session = next(get_db())  # Open a session

    print("Welcome to the Lesson Management System")

    while True:
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
            break

if __name__ == "__main__":
    main()
