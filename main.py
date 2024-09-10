from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# JWT configuration
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# SQLAlchemy setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./workout_tracker.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

# FastAPI app
app = FastAPI()

# Sign up endpoint
@app.post("/signup", response_model=Token)
def create_user(user: UserCreate, db: SessionLocal = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Login endpoint
@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: SessionLocal = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Create workout endpoint
@app.post("/workouts/")
def create_workout(workout: WorkoutCreate, db: SessionLocal = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_workout = Workout(
        user_id=current_user.id,
        exercise_id=workout.exercise_id,
        repetitions=workout.repetitions,
        sets=workout.sets,
        weight=workout.weight,
        scheduled_at=workout.scheduled_at,
        comments=workout.comments
    )
    db.add(new_workout)
    db.commit()
    return {"message": "Workout created successfully"}

# List workouts endpoint
@app.get("/workouts/")
def list_workouts(db: SessionLocal = Depends(get_db), current_user: User = Depends(get_current_user)):
    workouts = db.query(Workout).filter(Workout.user_id == current_user.id).all()
    return workouts
