from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
load_dotenv()


DB_URL: str = os.getenv("DB")

print(f"\n\nDB_URL = {DB_URL}\n\n")
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(
    
    bind=engine
)

Base = declarative_base()

db = SessionLocal()


def get_db():
    """
    Generator function that returns a SQLAlchemy session object.
    This function is used as a context manager to ensure the session is properly closed.
    Yields:
        Session: A SQLAlchemy session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()