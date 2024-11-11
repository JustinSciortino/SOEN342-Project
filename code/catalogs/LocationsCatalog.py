from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import Location, SpaceType

class LocationsCatalog:
    _instance = None

    def __init__(self, session: Session):
        self.session = session

    @classmethod
    def get_instance(cls, session: Session):
        if cls._instance is None:
            cls._instance = cls(session)
        return cls._instance
    
    def create_location(self, name: str, address: str, capacity: int, city: str, space_type: list[SpaceType]):
        existing_location = self.session.query(Location).filter(Location.name == name, 
                                                                Location.address == address,
                                                                Location.city == city, 
                                                                Location.space_type == [space.value for space in space_type]
                                                                ).first()
        if existing_location:
            raise ValueError(f"Location '{name}' located at {address} in {city} already exists")
        
        location = Location(name=name, address=address, capacity=capacity, city=city, space_type=space_type)

        if not location:
            raise ValueError("Location not created")
        
        self.session.add(location)
        self.session.commit()
        return location
    
    def get_location(self, city: str, name: str = None, address: str = None):
        location = None
        if name is None and address is None:
            location = self.session.query(Location).filter(Location.city == city).all()
        else:
            location = self.session.query(Location).filter(Location.city == city, 
                                                           Location.name == name, 
                                                           Location.address == address).first()
        if not location:
            raise ValueError(f"Location '{city}' does not exist")
        
        return location
    
    def get_location_by_id(self, _id: int):
        location = self.session.query(Location).filter(Location.id == _id).first()
        if not location:
            raise ValueError(f"Location with id '{_id}' does not exist")
        
        return location
    
    def add_timeslot(self, location: Location, timeslot: "Timeslot"):
        try:            
            location.schedule.add_timeslot(timeslot)
            self.session.commit()
            return True
        except IntegrityError as e:
            self.session.rollback()
            print(f"Error adding timeslot: {str(e)}")
            return False
        except Exception as e:
            self.session.rollback()
            print(f"An unexpected error occurred: {str(e)}")
            return False
        
    def get_all_locations(self):
        return self.session.query(Location).all()