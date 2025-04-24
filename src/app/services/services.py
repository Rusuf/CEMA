from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from datetime import date

from ..models.models import Program, Client, Enrollment
from ..models.schemas import ProgramCreate, ClientCreate, ProgramEnrollment, EnrollmentCreate

class ProgramService:
    @staticmethod
    def create_program(db: Session, program: ProgramCreate):
        """Create a new health program"""
        db_program = Program(name=program.name, description=program.description)
        
        try:
            db.add(db_program)
            db.commit()
            db.refresh(db_program)
            return db_program
        except IntegrityError:
            db.rollback()
            raise ValueError(f"Program with name '{program.name}' already exists")
    
    @staticmethod
    def get_programs(db: Session, skip: int = 0, limit: int = 100):
        """Get all health programs"""
        return db.query(Program).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_program_by_id(db: Session, program_id: int):
        """Get a program by ID"""
        return db.query(Program).filter(Program.id == program_id).first()


class ClientService:
    @staticmethod
    def create_client(db: Session, client: ClientCreate):
        """Register a new client"""
        db_client = Client(
            name=client.name,
            date_of_birth=client.date_of_birth,
            contact_info=client.contact_info
        )
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return db_client
    
    @staticmethod
    def get_clients(db: Session, skip: int = 0, limit: int = 100):
        """Get all clients"""
        return db.query(Client).offset(skip).limit(limit).all()
    
    @staticmethod
    def search_clients(db: Session, search: str, skip: int = 0, limit: int = 100):
        """Search clients by name or contact info"""
        return db.query(Client).filter(
            or_(
                Client.name.ilike(f"%{search}%"),
                Client.contact_info.ilike(f"%{search}%")
            )
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_client_by_id(db: Session, client_id: int):
        """Get a client by ID"""
        return db.query(Client).filter(Client.id == client_id).first()
    
    @staticmethod
    def get_client_profile(db: Session, client_id: int):
        """Get a client profile with their program enrollments"""
        client = db.query(Client).filter(Client.id == client_id).first()
        
        if client:
            enrollments = db.query(
                Enrollment.program_id,
                Program.name.label("program_name"),
                Enrollment.enrollment_date
            ).join(
                Program, Enrollment.program_id == Program.id
            ).filter(
                Enrollment.client_id == client_id
            ).all()
            
            program_enrollments = [
                ProgramEnrollment(
                    program_id=enrollment.program_id,
                    program_name=enrollment.program_name,
                    enrollment_date=enrollment.enrollment_date
                )
                for enrollment in enrollments
            ]
            
            setattr(client, "enrollments", program_enrollments)
            
        return client


class EnrollmentService:
    @staticmethod
    def enroll_client(db: Session, client_id: int, enrollment: EnrollmentCreate):
        """Enroll a client in a health program"""
        # Verify client exists
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise ValueError(f"Client with ID {client_id} not found")
        
        # Verify program exists
        program = db.query(Program).filter(Program.id == enrollment.program_id).first()
        if not program:
            raise ValueError(f"Program with ID {enrollment.program_id} not found")
        
        # Create enrollment
        db_enrollment = Enrollment(
            client_id=client_id,
            program_id=enrollment.program_id,
            enrollment_date=date.today()
        )
        
        try:
            db.add(db_enrollment)
            db.commit()
            db.refresh(db_enrollment)
            return db_enrollment
        except IntegrityError:
            db.rollback()
            raise ValueError(f"Client {client_id} is already enrolled in program {enrollment.program_id}")
    
    @staticmethod
    def get_client_enrollments(db: Session, client_id: int):
        """Get all enrollments for a client"""
        return db.query(Enrollment).filter(Enrollment.client_id == client_id).all() 