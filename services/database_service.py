from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_NAME = os.getenv('DATABASE')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.client import Base

DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@localhost/{DATABASE_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
