from fastapi import APIRouter, Depends, HTTPException, Security, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Callable, Any
from functools import wraps
import traceback
import logging

from ..database.database import get_db
from ..services.services import ProgramService, ClientService, EnrollmentService
from ..models.schemas import Program, ProgramCreate, Client, ClientCreate, ClientProfile, Enrollment, EnrollmentCreate, ErrorResponse, ProgramEnrollment
from ..services.auth import get_api_key

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create program router
program_router = APIRouter(
    prefix="/programs",
    tags=["programs"],
    responses={404: {"model": ErrorResponse}}
)

# Create client router
client_router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    responses={404: {"model": ErrorResponse}}
)

# Create enrollment router
enrollment_router = APIRouter(
    prefix="/clients/{client_id}/enrollments",
    tags=["enrollments"],
    responses={404: {"model": ErrorResponse}}
)

# Create API router
api_router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"model": ErrorResponse}}
)

# Helper function for error handling
def handle_exceptions(func: Callable) -> Callable:
    """Decorator to handle common exceptions in route handlers"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            if "not found" in str(e):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"Unexpected error: {str(e)}"
            )
    return wrapper

# Helper function to get client profile with validation
def get_validated_client_profile(client_id: int, db: Session) -> ClientProfile:
    """Get client profile and raise HTTPException if not found"""
    client = ClientService.get_client_profile(db, client_id)
    if client is None:
        raise HTTPException(status_code=404, detail=f"Client with ID {client_id} not found")
    return client

# ----- Program Routes -----

@program_router.post("/", response_model=Program, status_code=status.HTTP_201_CREATED)
@handle_exceptions
async def create_program(program: ProgramCreate, db: Session = Depends(get_db)):
    """Create a new health program"""
    return ProgramService.create_program(db, program)

@program_router.get("/", response_model=List[Program])
async def get_programs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all health programs"""
    return ProgramService.get_programs(db, skip, limit)

# ----- Client Routes -----

@client_router.post("/", response_model=Client, status_code=status.HTTP_201_CREATED)
@handle_exceptions
async def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    """Register a new client"""
    return ClientService.create_client(db, client)

# Define ClientWithEnrollments model for response
class ClientWithEnrollments(Client):
    enrollments: List[ProgramEnrollment] = []

@client_router.get("/", response_model=List[ClientWithEnrollments])
async def get_clients(search: Optional[str] = Query(None, description="Search by name or contact info"),
                skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Search or list registered clients"""
    if search:
        return ClientService.search_clients(db, search, skip, limit)
    return ClientService.get_clients(db, skip, limit)

@client_router.get("/{client_id}", response_model=ClientProfile)
async def get_client(client_id: int, db: Session = Depends(get_db)):
    """View a specific client's profile (including program enrollments)"""
    return get_validated_client_profile(client_id, db)

# ----- Enrollment Routes -----

@enrollment_router.post("/", response_model=Enrollment, status_code=status.HTTP_201_CREATED)
@handle_exceptions
async def enroll_client(client_id: int, enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    """Enroll a client in a program"""
    logger.info(f"Enrollment request received: client_id={client_id}, data={enrollment}")
    result = EnrollmentService.enroll_client(db, client_id, enrollment)
    logger.info(f"Enrollment successful: {result}")
    return result

# ----- API Routes (with authentication) -----

@api_router.get("/clients/{client_id}", response_model=ClientProfile)
async def get_client_profile_api(client_id: int, db: Session = Depends(get_db), api_key: str = Security(get_api_key)):
    """View a specific client's profile via secure API"""
    return get_validated_client_profile(client_id, db) 