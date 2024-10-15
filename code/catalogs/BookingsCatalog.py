from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Booking

class BookingsCatalog:
    _instance = None

    def __init__(self, session: Session):
        self.session = session

    @classmethod
    def get_instance(cls, session: Session):
        if cls._instance is None:
            cls._instance = cls(session)
        return cls._instance
    
    def create_booking(self):
        pass