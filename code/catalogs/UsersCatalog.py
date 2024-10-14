from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import User, Client, Instructor, Admin

class UsersCatalog:
    _instance = None

    def __init__(self, session: Session):
        self.session = session

    @classmethod
    def get_instance(cls, session: Session):
        if cls._instance is None:
            cls._instance = cls(session)
        return cls._instance
    
    def register_admin(self, name: str, password: str):
        existing_user = self.session.query(User).join(Admin).filter(User.name == name).first()

        if existing_user:
            raise ValueError(f"Admin with name '{name}' already exists")
        
        user = User(name=name, password=password, type="Admin")
        self.session.add(user)
        self.session.flush()

        admin = Admin(id=user.id)
        self.session.add(admin)
        self.session.commit()
        return admin
    
    def login(self, name: str, password: str):
        user = self.session.query(User).filter(User.name == name).first()
        
        if user and user.password == password:
            if user.type == "Client":
                client = self.session.query(Client).filter(Client.id == user.id, Client.phone_number == phone_number).first()
                return client if client else None
            elif user.type == "Instructor":
                instructor = self.session.query(Instructor).filter(Instructor.id == user.id, Instructor.phone_number == phone_number).first()
                return instructor if instructor else None
            elif user.type == "Admin":
                admin = self.session.query(Admin).filter(Admin.id == user.id).first()
                return admin if admin else None
        return None