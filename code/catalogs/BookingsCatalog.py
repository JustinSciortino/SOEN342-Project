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
    
    def get_booking(self, booking_id: int) -> Booking:
        booking = self.session.query(Booking).filter_by(id=booking_id).first()
        return booking
    
    def cancel_booking_(self, booking_id: int):
        booking = self.session.query(Booking).filter_by(id=booking_id).first()
        if not booking:
            raise ValueError(f"Booking with id '{booking_id}' does not exist")
        #booking.cancel()
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
    
    def cancel_booking(self, client: "Client", booking: "Booking", minor_id: int = None):

        try:
            client.bookings.remove(booking)

            if minor_id:
                minor = self.session.query(Minor).filter(Minor.id == minor_id).first()
                if minor:
                    minor.bookings.remove(booking)

            booking.offering.bookings.remove(booking) #! Can also optionally call the cancel() method in Booking class

            self.session.delete(booking) #! Do we want to delete the booking from the database or mark it as cancelled? 
                                    #!Something to ask CC or TA because if an Offering is cancelled, the associated bookings are marked as cancelled but neither offering nor bookings are deleted
                                    #! Idea is that the user should have some idea that the booking was cancelled and that it just didnt disappear like that

            self.session.commit()

            print(f"Booking {booking.id} has been successfully canceled.") #!Booking will be deleted so we cant get the id

        except ValueError:
            self.session.rollback()
            print(f"An error occurred while trying to cancel the booking.")

    def get_minor_bookings(self, minor_id: int):
        return self.session.query(Booking).filter_by(minor_id=minor_id).all()