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

    def get_booking(self, booking_id: int) -> Booking:
        booking = self.session.query(Booking).filter_by(id=booking_id).first()
        return booking
    
    def cancel_booking(self, booking_id: int):
        booking = self.session.query(Booking).filter_by(id=booking_id).first()
        if not booking:
            raise ValueError(f"Booking with id '{booking_id}' does not exist")
        booking.cancel()
        self.session.commit()
        return booking