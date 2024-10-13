from db.models import Client, Instructor, Admin, Offering, Location, Booking
from sqlalchemy.orm import Session

# LOGIN FUNCTIONS

def login_client(client_id, db: Session):
    """Login for clients."""
    return db.query(Client).filter(Client.id == client_id).first()

def login_instructor(instructor_id, db: Session):
    """Login for instructors."""
    return db.query(Instructor).filter(Instructor.id == instructor_id).first()

def login_admin(admin_id, db: Session):
    """Login for admins."""
    return db.query(Admin).filter(Admin.id == admin_id).first()

# SIGNUP PROCESS FUNCTIONS

def signup_client_process(name, phone_number, email, is_underage, guardian_id, db: Session):
    """Process for signing up a client."""
    return signup_client(name, phone_number, email, is_underage, guardian_id, db)

def signup_instructor_process(name, phone_number, email, specialization, available_cities, db: Session):
    """Process for signing up an instructor."""
    return register_instructor(name, phone_number, email, specialization, available_cities, db)

# PUBLIC FUNCTIONS

def view_offerings(db: Session):
    """View all available offerings. Filter by teaching status if necessary."""
    return db.query(Offering).filter(Offering.is_available == True, Offering.status == "Teaching").all()

def signup_client(name, phone_number, email, is_underage, guardian_id, db: Session):
    """Sign up a new client."""
    client = Client(name=name, phone_number=phone_number, email=email, is_underage=is_underage, guardian_id=guardian_id)
    db.add(client)
    db.commit()
    return client

def signup_admin(name, phone_number, db: Session):
    """Sign up a new admin."""
    admin = Admin(name=name, phone_number=phone_number)
    db.add(admin)
    db.commit()
    return admin

# CLIENT FUNCTIONS

def view_client_bookings(client_id, db: Session):
    """View all bookings for a client."""
    return db.query(Booking).filter(Booking.client_id == client_id).all()

def book_offering(client_id, offering_id, db: Session):
    """Book an offering for a client."""
    offering = db.query(Offering).filter(Offering.id == offering_id).first()
    if offering and offering.is_available:
        booking = Booking(client_id=client_id, offering_id=offering_id)
        offering.is_available = False  # Mark offering as booked
        db.add(booking)
        db.commit()
        return booking
    else:
        print("Offering not available or does not exist.")
        return None

def cancel_booking(client_id, booking_id, db: Session):
    """Cancel a booking for a client."""
    booking = db.query(Booking).filter(Booking.id == booking_id, Booking.client_id == client_id).first()
    if booking:
        offering = db.query(Offering).filter(Offering.id == booking.offering_id).first()
        if offering:
            offering.is_available = True  # Mark offering as available again
        db.delete(booking)
        db.commit()
    else:
        print("Booking not found or client does not match.")

# INSTRUCTOR FUNCTIONS

def view_instructor_offerings(instructor_id, db: Session):
    """View all offerings for a specific instructor."""
    return db.query(Offering).filter(Offering.instructor_id == instructor_id).all()

def teach_offering(instructor_id, offering_id, db: Session):
    """Set an offering as 'Teaching' for the instructor."""
    offering = db.query(Offering).filter(Offering.id == offering_id, Offering.instructor_id == instructor_id).first()
    if offering:
        offering.status = "Teaching"
        db.commit()
        return offering
    else:
        print("Offering not found or instructor does not match.")
        return None

def register_instructor(name, phone_number, email, specialization, available_cities, db: Session):
    """Register a new instructor."""
    instructor = Instructor(name=name, phone_number=phone_number, email=email, specialization=specialization, available_cities=available_cities)
    db.add(instructor)
    db.commit()
    return instructor

# ADMIN FUNCTIONS

def create_offering(location, lesson_type, start_time, end_time, instructor_id, db: Session):
    """Create a new offering."""
    offering = Offering(location=location, lesson_type=lesson_type, start_time=start_time, end_time=end_time, instructor_id=instructor_id, is_available=True, status="Available")
    db.add(offering)
    db.commit()

def view_client_bookings_by_admin(db: Session):
    """Admin view of all client bookings."""
    return db.query(Booking).all()

def delete_account(account_id, db: Session):
    """Delete a client or instructor account."""
    client = db.query(Client).filter(Client.id == account_id).first()
    instructor = db.query(Instructor).filter(Instructor.id == account_id).first()
    if client:
        db.delete(client)
    elif instructor:
        db.delete(instructor)
    else:
        print("Account not found.")
    db.commit()

def modify_offering(offering_id, db: Session, **kwargs):
    """Modify an existing offering."""
    offering = db.query(Offering).filter(Offering.id == offering_id).first()
    if offering:
        for key, value in kwargs.items():
            if hasattr(offering, key):
                setattr(offering, key, value)
        db.commit()
    else:
        print("Offering not found.")

def cancel_offering(offering_id, db: Session):
    """Cancel an existing offering."""
    offering = db.query(Offering).filter(Offering.id == offering_id).first()
    if offering:
        offering.is_available = False
        offering.status = "Cancelled"  # You can use 'Cancelled' as a status to track cancellations
        db.commit()
    else:
        print("Offering not found.")
