import os
from sqlmodel import create_engine, Session
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Determine the environment
environment = os.getenv("ENV", "dev")

# Set the database URL based on the environment
if environment == "prod":
    DATABASE_URL = os.getenv("DATABASE_URL_PROD")
else:
    DATABASE_URL = os.getenv("DATABASE_URL_DEV")

# Ensure DATABASE_URL is a string and not None
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create the engine
engine = create_engine(DATABASE_URL)


def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
