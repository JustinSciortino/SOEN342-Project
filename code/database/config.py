from sqlalchemy import create_engine, Column, Integer, String, inspect
from sqlalchemy.orm import sessionmaker, declarative_base


# Database connection URL
DATABASE_URL = "postgresql://postgres:<<ENTERPASSWORDHERE>>@localhost:5432/lesson_management"
DATABASE_URL_DOCKER = 'postgresql://user:password@localhost:5432/lesson_management'

# Create engine and session
engine = create_engine(DATABASE_URL_DOCKER)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for your models
Base = declarative_base()

def create_tables():
    import models
    try:
        inspector = inspect(engine)
        for table_name in inspector.get_table_names():
            engine.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
        Base.metadata.create_all(bind=engine)
        #print("Tables created successfully!")
    except Exception as e:
        print(f"An error occurred while creating tables: {e}")

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()