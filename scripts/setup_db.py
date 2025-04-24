import os
import sqlite3
from dotenv import load_dotenv

def setup_database():
    """Create SQLite database for the BHIS application"""
    load_dotenv()
    
    # Get database path from environment
    db_url = os.getenv("DATABASE_URL", "sqlite:///bhis.db")
    
    # Extract the database path from the URL
    if db_url.startswith("sqlite:///"):
        db_path = db_url.replace("sqlite:///", "")
    else:
        print(f"Warning: Non-SQLite URL detected ({db_url}). Using SQLite anyway.")
        db_path = "bhis.db"
    
    print(f"Setting up SQLite database at '{db_path}'...")
    
    # SQLite database will be created automatically when accessed
    # Just create a simple test connection to verify it works
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Test the connection with a simple query
        cursor.execute("SELECT sqlite_version();")
        version = cursor.fetchone()
        print(f"SQLite database ready (version: {version[0]})")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error setting up database: {str(e)}")
        return False

if __name__ == "__main__":
    setup_database() 