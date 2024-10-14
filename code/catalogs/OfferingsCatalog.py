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
    
    #! To be validated/verified
    def create_offering(self, name: str, offering_type: OfferingType, location_id: int, instructor_id: int, schedule_id: int):
        existing_offering = self.session.query(Offering).filter(Offering.name == name, 
                                                                 Offering.location_id == location_id,
                                                                 Offering.instructor_id == instructor_id,
                                                                 Offering.schedule_id == schedule_id
                                                                 ).first()
        if existing_offering:
            raise ValueError(f"Offering '{name}' already exists")
        
        offering = Offering(name=name, offering_type=offering_type, location_id=location_id, instructor_id=instructor_id, schedule_id=schedule_id)

        if not offering:
            raise ValueError("Offering not created")
        
        self.session.add(offering)
        self.session.commit()
        return offering