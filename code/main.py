from catalogs.UserCatalog import UserCatalog

def main():
    user_catalog = UserCatalog.get_instance()

    while True:
        print("\n1. Register")
        print("2. Get User")
        print("3. Remove User")
        print("4. List All Users")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter your name: ")
            password = input("Enter your password: ")
            try:
                user_catalog.add_user(name, password)
                print("User registered successfully!")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '2':
            name = input("Enter user name to retrieve: ")
            user = user_catalog.get_user(name)
            if user:
                print(f"User found: {user}")
            else:
                print("User not found.")
        elif choice == '3':
            name = input("Enter user name to remove: ")
            try:
                user_catalog.remove_user(name)
                print("User removed successfully!")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '4':
            users = UserCatalog.get_all_users()
            print("All users:")
            for user in users:
                print(user)
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()