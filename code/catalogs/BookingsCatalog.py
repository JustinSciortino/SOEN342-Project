from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Booking, Client, Offering, Minor

class BookingsCatalog:
    _instance = None

    def __init__(self, session: Session):
        self.session = session

    @classmethod
    def get_instance(cls, session: Session):
        if cls._instance is None:
            cls._instance = cls(session)
        return cls._instance
    
    def cancel_booking(self, booking):
        if not booking:
            raise ValueError("Booking does not exist")
        
        offering = booking.get_offering() 
        print(f"\nOffering {offering.get_id()} is now available.")
        if offering.get_lesson().get_type().value == 'private':
            offering.set_status("Available") 
        else:
            if len(offering.get_bookings()) < offering.get_lesson().get_capacity():
                offering.set_status("Available")
        
        self.session.delete(booking)
        self.session.commit()
        return booking

    def create_booking(self, client: "Client", offering: "Offering", minor: "Minor" = None):
        try:
            if minor:
                minor = self.session.merge(minor)
            client = self.session.merge(client)
            offering = self.session.merge(offering)
            
            new_booking = Booking(client=client, offering=offering, minor=minor)

            if offering.get_lesson().get_type().value == 'private':
                offering.set_status("Not-Availiable")
            else:
                if len(offering.get_bookings()) == offering.get_lesson().get_capacity():
                    offering.set_status("Not-Available")

            self.session.add(new_booking)

            self.session.commit()

            print(f"\nBooking for offering {offering.id} successfully created!")
            return new_booking

        except IntegrityError:
            self.session.rollback()
            print("An error occurred while trying to create the booking.")
            return None

    def get_client_bookings(self, client: "Client"):
        return self.session.query(Booking).filter(Booking.client_id == client.get_id()).all()