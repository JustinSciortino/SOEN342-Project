from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

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
    
    def create_offering(self, location: "Location", capacity: int, timeslot: "Timeslot", offering_type: OfferingType):
        offering = Offering(location=location, capacity=capacity, timeslot=timeslot, offering_type=offering_type)

        if not offering:
            raise ValueError("Offering not created")
        
        self.session.add(offering)
        self.session.commit()
        return offering
    
    def get_all_offerings(self, city: str = None, space_type: "SpaceType" = None, _type: OfferingType = None, is_admin: bool = False):
        query = self.session.query(Offering).join(Offering.location)

        if is_admin:
            if city is not None:
                query = query.filter(Location.city == city)
            if space_type is not None:
                query = query.filter(Location.space_type == space_type)
            if _type is not None:
                query = query.filter(Offering.type == _type)
        else:
            query = query.filter(Offering.is_available == True)
            if city is not None:
                query = query.filter(Location.city == city)
            if space_type is not None:
                query = query.filter(Location.space_type == space_type)
            if _type is not None:
                query = query.filter(Offering.type == _type)

        return query.all()