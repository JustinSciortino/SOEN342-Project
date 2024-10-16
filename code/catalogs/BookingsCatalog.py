from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Booking, Client, Offering

class BookingsCatalog:
    _instance = None

    def __init__(self, session: Session):
        self.session = session

    @classmethod
    def get_instance(cls, session: Session):
        if cls._instance is None:
            cls._instance = cls(session)
        return cls._instance

    def create_booking(self, client: "Client", offering: "Offering"):
        try:
            new_booking = Booking(client=client, status="Booked", active=True, is_cancelled=False, offering=offering)

            self.session.add(new_booking)
            self.session.commit()

            offering.add_booking(new_booking)
            self.session.commit()

            client.bookings.append(new_booking)
            self.session.commit()

            print(f"\nBooking for offering {offering.id} successfully created!")
            return new_booking

        except IntegrityError:
            self.session.rollback()
            print("An error occurred while trying to create the booking.")
            return None

    def get_client_bookings(self, client: "Client"):
        return self.session.query(Booking).filter(Booking.client_id == client.get_id()).all()
    
    def cancel_booking(self, client: "Client", booking: "Booking"):

        try:
            # Remove the booking from the client's list
            client.bookings.remove(booking)

            # Remove the booking from the offering's list
            booking.offering.bookings.remove(booking)

            # Delete the booking from the database
            self.session.delete(booking)
            self.session.commit()

            print(f"Booking {booking.id} has been successfully canceled.")

        except ValueError:
            self.session.rollback()
            print(f"An error occurred while trying to cancel the booking.")