# database.py
from sqlalchemy import create_engine, Column, Integer, String, Time, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

# Database setup
DATABASE_URL = "sqlite:///food_data.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the FoodData model
class FoodData(Base):
    __tablename__ = "food_data"  # Fixed typo here
    id = Column(Integer, primary_key=True, index=True)
    restaurant_name = Column(String, index=True)
    food_description = Column(String)
    quantity = Column(Integer)
    pickup_time = Column(Time)
    location = Column(String)
    address = Column(String)
    contact_info = Column(String)
    date_submitted = Column(DateTime, default=datetime.utcnow)

# Define the RestaurantUser model
class RestaurantUser(Base):
    __tablename__ = "restaurant_users"  # Fixed typo here
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

# Create the tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hashes the given password."""
    return pwd_context.hash(password)

def create_user(username: str, password: str):
    """Creates a new user with the given username and hashed password."""
    hashed_password = hash_password(password)
    user = RestaurantUser(username=username, password=hashed_password)
    session = SessionLocal()
    session.add(user)
    try:
        session.commit()
        return True, f"User '{username}' created successfully."
    except IntegrityError:
        session.rollback()
        return False, f"Username '{username}' already exists."
    finally:
        session.close()
