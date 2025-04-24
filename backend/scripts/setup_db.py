import sys
import os
from pathlib import Path
import sqlite3

# Add the parent directory to path so we can import the app modules
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from app.database.database import Base, engine

def setup_db():
    """Create a fresh database with all tables"""
    print("Setting up a fresh database...")
    
    # Delete existing SQLite file if it exists
    db_path = os.path.join(Path(__file__).parent.parent, 'bhis.db')
    if os.path.exists(db_path):
        print(f"Removing existing database file at {db_path}")
        os.remove(db_path)
    
    # Create tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database setup completed successfully.")

if __name__ == "__main__":
    setup_db() 