from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.User import User, Base

class UserCatalog:
    #both of the attributes below are static
    __instance = None #Private attribute if it starts with __ (2 underscores)
    users = {}  

    def __init__(self):
        self.engine = create_engine('postgresql://user:password@db:5432/userdb')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self._load_users()

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def _load_users(self):
        session = self.Session()
        all_users = session.query(User).all()
        for user in all_users:
            UserCatalog._users[user.name] = user
        session.close()

    def add_user(self, name, password):
        session = self.Session()
        new_user = User(name=name, password=password)
        session.add(new_user)
        session.commit()
        session.close()


    def get_user(self, name):
        return UserCatalog.users.get(name)

    def remove_user(self, name):
        if name not in UserCatalog.users:
            raise ValueError(f"User with name '{name}' does not exist")

        session = self.Session()
        user = session.query(User).filter_by(name=name).first()
        if user:
            session.delete(user)
            session.commit()
            del UserCatalog.users[name]
        session.close()

    @classmethod  #Same as a statci method
    def get_all_users(cls):
        return list(cls.users.values()) #cls refers to the class