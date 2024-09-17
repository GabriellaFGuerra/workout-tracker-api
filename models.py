from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from database_setup import *

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Exercise(Base):
    __tablename__ = "exercises"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    category = Column(String)

class Workout(Base):
    __tablename__ = "workouts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    repetitions = Column(Integer)
    sets = Column(Integer)
    weight = Column(Float)
    scheduled_at = Column(DateTime, index=True)
    comments = Column(String, nullable=True)
    user = relationship("User")
    exercise = relationship("Exercise")

# Create database tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class ExerciseCreate(BaseModel):
    name: str
    description: str
    category: str

class WorkoutCreate(BaseModel):
    exercise_id: int
    repetitions: int
    sets: int
    weight: Optional[float]
    scheduled_at: Optional[datetime]
    comments: Optional[str]