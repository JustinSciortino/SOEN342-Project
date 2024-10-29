from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import User, Client, Instructor, Admin, SpecializationType, Minor


class UsersCatalog:
    _instance = None

    def __init__(self, session: Session):
        self.session = session

    @classmethod
    def get_instance(cls, session: Session):
        if cls._instance is None:
            cls._instance = cls(session)
        return cls._instance
    
    #TODO Register a client
    
    def register_admin(self, name: str, password: str):
        #existing_user = self.session.query(User).join(Admin).filter(User.name == name).first() # Checks for users who are also admins
        existing_user = self.session.query(User).filter(User.name == name).first() #Checks for all users regardless of thei roles
        if existing_user:
            raise ValueError(f"Admin with name '{name}' already exists")
        
        admin = Admin(name=name, password=password)

        if not admin:
            raise ValueError("Admin not created")
        
        self.session.add(admin)
        self.session.commit()
        return admin
    
    def register_instructor(self, name: str, password: str, phone_number: str, specialization: list[SpecializationType], available_cities: list[str]):
        existing_user = self.session.query(User).filter(User.name == name).first()
        
        if existing_user:
            raise ValueError(f"Instructor with name '{name}' already exists")
        
        existing_instructor = self.session.query(Instructor).filter(Instructor.phone_number == phone_number).first()
    
        if existing_instructor:
            raise ValueError(f"Instructor with phone number '{phone_number}' already exists")
        
        if not all(isinstance(spec, SpecializationType) for spec in specialization):
            raise ValueError("All specializations must be of type SpecializationType")

        instructor = Instructor(name=name, password=password, phone_number=phone_number, specialization=specialization, available_cities=available_cities)

        if not instructor:
            raise ValueError("Instructor not created")
        
        self.session.add(instructor)
        self.session.commit()
        return instructor
    
    def register_client(self, name: str, phone_number: str, password: str, is_legal_guardian: bool):
        existing_user = self.session.query(User).filter(User.name == name).first()

        if existing_user:
            raise ValueError(f"User with name '{name}' already exists")
        
        existing_client = self.session.query(Client).filter(Client.phone_number == phone_number).first()

        if existing_client:
            raise ValueError(f"User with phone number '{phone_number}' already exists")
        
        client = Client(name=name, phone_number=phone_number, password=password, is_legal_guardian=is_legal_guardian)

        if not client:
            raise ValueError("Client not created")
        
        self.session.add(client)
        self.session.commit()
        return client

    
    def login(self, name: str, password: str, phone_number: str=None):
        user = self.session.query(User).filter(User.name == name).first()

        if not user:
            raise ValueError(f"\nUser with name '{name}' does not exist")
        
        if user.password == password:
            if user.type == "client":
                client = self.session.query(Client).filter(Client.id == user.id, Client.phone_number == phone_number).first()
                return client if client else None
            elif user.type == "instructor":
                instructor = self.session.query(Instructor).filter(Instructor.id == user.id, Instructor.phone_number == phone_number).first()
                return instructor if instructor else None
            elif user.type == "admin":
                admin = self.session.query(Admin).filter(Admin.id == user.id).first()
                return admin if admin else None
        return None
    
    def has_admin(self):
        return self.session.query(Admin).first() is not None
    #! Needs to be modified, needs to cancel all bookings associated with the Instructor Offering
    #! Needs to be modified, needs to cancel all bookings associated with the Client
    def delete_user(self, name: str=None, id: int=None):
        if not name and not id:
            raise ValueError("Name or id must be provided")
        if id:
            user = self.session.query(User).filter(User.id == id).first()
        else:
            user = self.session.query(User).filter(User.name == name).first()
        if not user:
            raise ValueError(f"User with name '{name}' does not exist")
        
        if user.get_type() == "admin":
            raise ValueError("Cannot delete admin")
        
        self.session.delete(user)
        self.session.commit()
        return user
    
    def get_all_users(self):
        return self.session.query(User).all()
    
    def get_user(self, name: str):
        user = self.session.query(User).filter(User.name == name).first()
        if not user:
            raise ValueError(f"User with name '{name}' does not exist")
        
        return user
    
    def get_user_by_id(self, id: int):
        user = self.session.query(User).filter(User.id == id).first()
        if not user:
            raise ValueError(f"User with id '{id}' does not exist")
        
        return user

    def create_and_add_minor(self, guardian: "Client", name: str, age: int):
        minor = Minor(guardian=guardian, name=name, age=age)
        self.session.add(minor)
        self.session.commit()

    def get_client_by_id(self, client_id: int):
        return self.session.query(Client).filter(Client.id == client_id).first()
    
    def update_instructor(self, instructor):
        try:
            self.session.add(instructor) 
            self.session.commit()  # Save the changes to the instructor
            print(f"Instructor {instructor.name} has been updated successfully.")
        except Exception as e:
            self.session.rollback()  # Rollback if there's an error
            raise ValueError(f"Failed to update instructor: {str(e)}")