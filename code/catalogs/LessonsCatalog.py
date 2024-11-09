from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Lesson, LessonType, Location, Timeslot, SpecializationType

class LessonsCatalog:
    _instance = None

    def __init__(self, session: Session):
        self.session = session

    @classmethod
    def get_instance(cls, session: Session):
        if cls._instance is None:
            cls._instance = cls(session)
        return cls._instance
    
    def create_lesson(self, location: "Location", capacity: int, timeslot: "Timeslot", lesson_type: LessonType, specialization: "SpecializationType"):
        lesson = Lesson(type=lesson_type, specialization=specialization, location=location, capacity=capacity, timeslot=timeslot)

        if not lesson:
            raise ValueError("Lesson not created")
        
        self.session.add(lesson)
        self.session.commit()
        return lesson
    
    def admin_get_all_lessons(self, city: str = None, specialization: "SpecializationType" = None, _type: LessonType = None):
        query = self.session.query(Lesson).join(Lesson.location)

        if city is not None:
            query = query.filter(Location.city == city)

        if specialization is not None:
            query = query.filter(Lesson.specialization == specialization.value)

        if _type is not None:
            query = query.filter(Lesson.type == _type)
        
        return query.all()
    
    def get_lesson_by_id(self, _id: int):
        lesson = self.session.query(Lesson).filter(Lesson.id == _id).first()
        if not lesson:
            raise ValueError(f"Lesson with id '{_id}' does not exist")
        
        return lesson
    
    def cancel_lesson(self, lesson):
        self.session.delete(lesson)
        self.session.commit()

    def get_available_lessons_without_offering(self, cities, specializations):
        return (
            self.session.query(Lesson)
            .join(Lesson.location)
            .outerjoin(Lesson.offerings)
            .filter(
                Location.city.in_(cities),
                Lesson.specialization.in_(specializations),
                Lesson.offerings == None
            )
            .all()
        )