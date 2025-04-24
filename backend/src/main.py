import uvicorn
import os
import sys

# Add the backend directory to the path for consistent imports
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.insert(0, backend_dir)

if __name__ == "__main__":
    # Run the application with hot-reload enabled
    print("Starting BHIS application...")
    uvicorn.run("src.app.main:app", host="0.0.0.0", port=8000, reload=True) 