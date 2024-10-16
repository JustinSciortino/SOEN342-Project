from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from models import Offering, OfferingType, Location, Timeslot, SpecializationType

class OfferingsCatalog:
    _instance = None

    def __init__(self, session: Session):
        self.session = session

    @classmethod
    def get_instance(cls, session: Session):
        if cls._instance is None:
            cls._instance = cls(session)
        return cls._instance
    
    def create_offering(self, location: "Location", capacity: int, timeslot: "Timeslot", offering_type: OfferingType, specialization: "SpecializationType"):
        offering = Offering(location=location, capacity=capacity, timeslot=timeslot, offering_type=offering_type, specialization=specialization)

        if not offering:
            raise ValueError("Offering not created")
        
        self.session.add(offering)
        self.session.commit()
        return offering

    def get_available_offerings_for_instructor(self, instructor):
        return self.session.query(Offering).filter(
            Offering.location.city.in_(instructor.available_cities),  
            Offering.specialization.in_(instructor.specialization),    
            Offering.instructor_id == None  
        ).all()

    def get_offerings_by_instructor_id(self, instructor_id: int):
        return self.session.query(Offering).filter(Offering.instructor_id == instructor_id).all()
      
    def get_all_offerings(self, city: str = None, specialization: "SpecializationType" = None, _type: OfferingType = None, is_admin: bool = False):
        query = self.session.query(Offering).join(Offering.location)

        if is_admin:
            if city is not None:
                query = query.filter(Location.city == city)
            if specialization is not None:
                query = query.filter(Offering.specialization == specialization.value)
            if _type is not None:
                query = query.filter(Offering.type == _type)
        else:
            query = query.filter(Offering.is_available == True)
            if city is not None:
                query = query.filter(Location.city == city)
            if specialization is not None:
                query = query.filter(Offering.specialization == specialization.value)
            if _type is not None:
                query = query.filter(Offering.type == _type)

        return query.all()

    def has_time_conflict(self, new_offering):
        for offering in self.offerings:
            if (offering.timeslot.start_date <= new_offering.timeslot.end_date and
                new_offering.timeslot.start_date <= offering.timeslot.end_date):
                if (offering.timeslot.start_time < new_offering.timeslot.end_time and
                    new_offering.timeslot.start_time < offering.timeslot.end_time):
                    return True
        return False
    
        def get_offering_by_id(self, _id: int):
            offering = self.session.query(Offering).filter(Offering.id == _id).first()
            if not offering:
                raise ValueError(f"Offering with id '{_id}' does not exist")
            
            return offering
        
        def cancel_offering(self, offering: Offering):
            offering.cancel_offering()
            self.session.commit()
            return offering

    def get_offerings_with_instructor(self):
        return self.session.query(Offering).filter(Offering.instructor_id.isnot(None)).all()
