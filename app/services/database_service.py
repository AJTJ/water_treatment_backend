import os
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    # declarative_base,
    Session as SQLAlchemySession,
    DeclarativeBase,
    # MappedAsDataclass,
)
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Load the database URL from environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://username:password@localhost:5432/database_name",
)

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base class for models
# Base = declarative_base()
# NOTE: Apparently using the declarative_base() function is not working as well
class Base(DeclarativeBase):
    pass


# TODO: Make all models dataclasses
# class Base(DeclarativeBase, MappedAsDataclass)
# pass


# Function to create a new session
def get_session() -> SQLAlchemySession:
    return SessionLocal()
