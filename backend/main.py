import uvicorn
import sys
import os

# Add the current directory to the Python path for consistent imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import the FastAPI app
from app.main import app

if __name__ == "__main__":
    # Run the application with hot-reload enabled
    print("Starting BHIS application...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 