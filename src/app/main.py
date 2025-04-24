from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .database.database import engine, Base
from .routes.routes import program_router, client_router, enrollment_router, api_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Basic Health Information System",
    description="A prototype system for managing health program clients",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(program_router)
app.include_router(client_router)
app.include_router(enrollment_router)
app.include_router(api_router)

# Custom exception handler
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail},
        )
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Basic Health Information System API",
        "docs": "/docs"
    } 