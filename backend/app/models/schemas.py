from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from enum import Enum

# Gender enum
class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"

# Program schemas
class ProgramBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProgramCreate(ProgramBase):
    pass

class Program(ProgramBase):
    id: int
    
    class Config:
        from_attributes = True

# Client schemas
class ClientBase(BaseModel):
    name: str
    date_of_birth: date
    contact_info: Optional[str] = None
    gender: Optional[GenderEnum] = None

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    
    class Config:
        from_attributes = True

# Enrollment schemas
class EnrollmentBase(BaseModel):
    program_id: int

class EnrollmentCreate(EnrollmentBase):
    enrollment_date: Optional[date] = None

class ProgramInfo(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True

class Enrollment(EnrollmentBase):
    id: int
    client_id: int
    enrollment_date: date
    program: Optional[ProgramInfo] = None
    
    class Config:
        from_attributes = True

# Extended schemas for client with enrollments
class ProgramEnrollment(BaseModel):
    program_id: int
    program_name: str
    enrollment_date: date
    
    class Config:
        from_attributes = True

class ClientProfile(Client):
    enrollments: List[ProgramEnrollment] = []
    
    class Config:
        from_attributes = True

# Error response schema
class ErrorResponse(BaseModel):
    error: str 