from db.models import Client, Instructor, Admin, Offering, Location, Booking 
from sqlalchemy.orm import Session

# LOGIN FUNCTIONS

def login_client(client_id, db: Session):
    client = db.query(Client).filter(Client.id == client_id).first()
    return client if client else None

def login_instructor(instructor_id, db: Session):
    instructor = db.query(Instructor).filter(Instructor.id == instructor_id).first()
    return instructor if instructor else None

def login_admin(admin_id, db: Session):
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    return admin if admin else None

# SIGNUP PROCESS FUNCTIONS

def signup_client_process(name, phone, is_underage, guardian_id, db: Session):
    return signup_client(name, phone, is_underage, guardian_id, db)

def signup_instructor_process(name, phone, specialization, available_cities, db: Session):
    return register_instructor(name, phone, specialization, available_cities, db)

# PUBLIC

def view_offerings(db):
    return db.query(Offering).filter(Offering.is_available == True).all() # have to make it so they can only see ones that have teaching status 

def signup_client(name, phone, is_underage, guardian_id, db):
    client = Client(name=name, phone=phone, is_underage=is_underage, guardian_id=guardian_id)
    db.add(client)
    db.commit()
    return client

def signup_admin(name, phone, db):
    admin = Admin(name=name, phone=phone)
    db.add(admin)
    db.commit()
    return admin

# CLIENT

def view_client_bookings(client_id, db):
    return db.query(Booking).filter(Booking.client_id == client_id).all()

def book_offering(client_id, offering_id, db):
    offering = db.query(Offering).filter(Offering.id == offering_id).first()
    if offering and offering.is_available:
        booking = Booking(client_id=client_id, offering_id=offering_id)
        offering.is_available = False  # Mark offering as booked
        db.add(booking)
        db.commit()
        return booking
    return None

def cancel_booking(client_id, booking_id, db):
    booking = db.query(Booking).filter(Booking.id == booking_id, Booking.client_id == client_id).first()
    if booking:
        offering = db.query(Offering).filter(Offering.id == booking.offering_id).first()
        offering.is_available = True  # Mark offering as available again
        db.delete(booking)
        db.commit()

# INSTRUCTOR

def view_instructor_offerings(instructor_id, db):
    return db.query(Offering).filter(Offering.instructor_id == instructor_id).all()

def teach_offering(instructor_id, offering_id, db):
    offering = db.query(Offering).filter(Offering.id == offering_id, Offering.instructor_id == instructor_id).first()
    if offering:
        offering.status = "Teaching"
        db.commit()
        return offering
    return None

def register_instructor(name, phone, specialization, available_cities, db):
    instructor = Instructor(name=name, phone=phone, specialization=specialization, available_cities=available_cities)
    db.add(instructor)
    db.commit()
    return instructor

# ADMIN

def create_offering(location, lesson_type, start_time, end_time, instructor_id, db):
    offering = Offering(location=location, lesson_type=lesson_type, start_time=start_time, end_time=end_time, instructor_id=instructor_id, is_available=True)
    db.add(offering)
    db.commit()

def view_client_bookings_by_admin(db):
    return db.query(Booking).all()

def delete_account(account_id, db):
    client = db.query(Client).filter(Client.id == account_id).first()
    instructor = db.query(Instructor).filter(Instructor.id == account_id).first()
    if client:
        db.delete(client)
    elif instructor:
        db.delete(instructor)
    db.commit()

def modify_offering(offering_id, db, **kwargs):
    offering = db.query(Offering).filter(Offering.id == offering_id).first()
    if offering:
        for key, value in kwargs.items():
            setattr(offering, key, value)
        db.commit()

def cancel_offering(offering_id, db):
    offering = db.query(Offering).filter(Offering.id == offering_id).first()
    if offering:
        offering.is_available = False
        db.commit()
