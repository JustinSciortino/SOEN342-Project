from db.config import SessionLocal, get_db
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
                client_id = login_client(db)
                if client_id:
                    client_menu(client_id, db)
            elif user_type == "instructor":
                instructor_id = login_instructor(db)
                if instructor_id:
                    instructor_menu(instructor_id, db)
            elif user_type == "admin":
                admin_id = login_admin(db)
                if admin_id:
                    admin_menu(admin_id, db)

        elif choice == '2':
            # Sign up as client
            signup_client_process(db)

        elif choice == '3':
            # Sign up as instructor
            signup_instructor_process(db)

        elif choice == '4':
            # View public offerings
            offerings = view_offerings(db)
            for offering in offerings:
                print(offering)

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
            for offering in offerings:
                print(offering)

        elif choice == '2':
            offering_id = input("Enter Offering ID to book: ")
            book_offering(client_id, offering_id, db)

        elif choice == '3':
            bookings = view_client_bookings(client_id, db)
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
            for offering in offerings:
                print(offering)

        elif choice == '2':
            create_offering_process(db)

        elif choice == '3':
            account_id = input("Enter Account ID to delete: ")
            delete_account(account_id, db)

        elif choice == '4':
            bookings = view_client_bookings_by_admin(db)
            for booking in bookings:
                print(booking)

        elif choice == '5':
            offering_id = input("Enter Offering ID to modify: ")
            modify_offering_process(offering_id, db)

        elif choice == '6':
            offering_id = input("Enter Offering ID to cancel: ")
            cancel_offering(offering_id, db)

        elif choice == '7':
            break

if __name__ == "__main__":
    main()
