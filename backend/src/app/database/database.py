import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import pathlib

# Find the base directory (backend folder)
backend_dir = pathlib.Path(__file__).parent.parent.parent.parent.absolute()

# Load environment variables from backend/.env
dotenv_path = os.path.join(backend_dir, '.env')
load_dotenv(dotenv_path)

# Get database URL from environment 
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bhis.db")

# For SQLite URLs, make sure the path is absolute
if DATABASE_URL.startswith('sqlite:///'):
    # Extract the database path from the URL
    db_path = DATABASE_URL.replace('sqlite:///', '')
    
    # If it's not an absolute path, make it relative to the backend directory
    if not os.path.isabs(db_path):
        abs_db_path = os.path.join(backend_dir, db_path)
        DATABASE_URL = f"sqlite:///{abs_db_path}"

# Create SQLAlchemy engine with correct parameters based on DB type
if DATABASE_URL.startswith('sqlite'):
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 