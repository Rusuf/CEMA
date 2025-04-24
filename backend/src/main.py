import uvicorn

if __name__ == "__main__":
    # Run the application directly
    from app.main import app
    
    print("Starting BHIS application...")
    uvicorn.run(app, host="0.0.0.0", port=8000) 