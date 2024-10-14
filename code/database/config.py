from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database connection URL
DATABASE_URL = "postgresql://postgres:<<ENTERPASSWORDHERE>>@localhost:5432/lesson_management"
DATABASE_URL_DOCKER = 'postgresql://user:password@localhost:5432/lesson_management'

# Create engine and session
engine = create_engine(DATABASE_URL_DOCKER)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for your models
Base = declarative_base()

Base.metadata.drop_all(bind=engine)  # Drops the tables
Base.metadata.create_all(bind=engine)  # Recreates the tables