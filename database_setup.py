from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

SQLALCHEMY_DATABASE_URL = "sqlite:///./workout_tracker.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()