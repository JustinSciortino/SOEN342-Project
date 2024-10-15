from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import Offering, OfferingType

class OfferingsCatalog:
    _instance = None

    def __init__(self, session: Session):
        self.session = session

    @classmethod
    def get_instance(cls, session: Session):
        if cls._instance is None:
            cls._instance = cls(session)
        return cls._instance
    
    def create_offering(self, location: "Location", capacity: int, timeslot: "Timeslot", offering_type: OfferingType):
        offering = Offering(location=location, capacity=capacity, timeslot=timeslot, offering_type=offering_type)

        if not offering:
            raise ValueError("Offering not created")
        
        self.session.add(offering)
        self.session.commit()
        return offering
    
    def get_all_offerings(self, city: str = None, space_type: "SpaceType" = None, _type: OfferingType = None):
        if city is not None and space_type is not None and _type is not None:
            return self.session.query(Offering).filter(Offering.location.city == city, Offering.location.space_type == space_type, Offering.offering_type == _type).all()
        if city is not None and space_type is not None:
            return self.session.query(Offering).filter(Offering.location.city == city, Offering.location.space_type == space_type).all()
        if city is not None and _type is not None:
            return self.session.query(Offering).filter(Offering.location.city == city, Offering.offering_type == _type).all()
        if city:
            return self.session.query(Offering).filter(Offering.location.city == city).all()
        if space_type:
            return self.session.query(Offering).filter(Offering.location.space_type == space_type).all()
        if _type:
            return self.session.query(Offering).filter(Offering.offering_type == _type).all()
        return self.session.query(Offering).all()
    
    def get_available_offerings_for_instructor(self, instructor):
        return self.session.query(Offering).filter(
            Offering.location.city.in_(instructor.available_cities),  
            Offering.offering_type.in_(instructor.specialization),    
            Offering.instructor_id == None  
        ).all()

    def get_offerings_by_instructor_id(self, instructor_id: int):
        return self.session.query(Offering).filter(Offering.instructor_id == instructor_id).all()
