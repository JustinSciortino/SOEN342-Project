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