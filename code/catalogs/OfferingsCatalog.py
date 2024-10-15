from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from models import Offering, OfferingType, Location

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
    
    def get_offering_by_id(self, _id: int):
        offering = self.session.query(Offering).filter(Offering.id == _id).first()
        if not offering:
            raise ValueError(f"Offering with id '{_id}' does not exist")
        
        return offering
    
    def cancel_offering(self, offering: Offering):
        offering.cancel_offering()
        self.session.commit()
        return offering