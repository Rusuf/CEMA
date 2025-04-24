import uvicorn
import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

if __name__ == "__main__":
    print("Starting BHIS application...")
    uvicorn.run("src.app.main:app", host="0.0.0.0", port=8000) 