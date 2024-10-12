from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from abc import ABC, ABCMeta

Base = declarative_base()

class BaseModelMeta(DeclarativeMeta, ABCMeta):
    pass

class User(Base, ABC, metaclass=BaseModelMeta): #Format for when User is an abstract class, can also use @abstractmethod decorators above methods to make them abstract
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)  # In a real application, ensure this is hashed
    user_type = Column(String(50))