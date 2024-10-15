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
    
    def create_location(self, name: str, address: str, capacity: int, city: str, space_type: SpaceType):
        existing_location = self.session.query(Location).filter(Location.name == name, 
                                                                Location.address == address,
                                                                Location.city == city, 
                                                                Location.space_type == space_type
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
    
    def delete_location(self, city: str, name: str, address: str, _id: int = None): #! Needs to be fixed to delete based on id as well
        location = self.session.query(Location).filter(Location.city == city, 
                                                       Location.name == name, 
                                                       Location.address == address).first()
        if not location:
            raise ValueError(f"Location '{city}' does not exist")
        
        self.session.delete(location)
        self.session.commit()
        return location