from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from datetime import date, datetime

from ..models.models import Program, Client, Enrollment, Gender
from ..models.schemas import ProgramCreate, ClientCreate, ProgramEnrollment, EnrollmentCreate, ClientProfile, GenderEnum

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
    
    @staticmethod
    def verify_program_exists(db: Session, program_id: int):
        """Verify that a program exists and return it or raise a ValueError"""
        program = ProgramService.get_program_by_id(db, program_id)
        if not program:
            raise ValueError(f"Program with ID {program_id} not found")
        return program


class ClientService:
    @staticmethod
    def create_client(db: Session, client: ClientCreate):
        """Register a new client"""
        # Convert string gender value to enum
        gender_val = None
        if client.gender:
            if client.gender == "male":
                gender_val = Gender.male
            elif client.gender == "female":
                gender_val = Gender.female
            elif client.gender == "other":
                gender_val = Gender.other
            
        db_client = Client(
            name=client.name,
            date_of_birth=client.date_of_birth,
            contact_info=client.contact_info,
            gender=gender_val
        )
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return db_client
    
    @staticmethod
    def _get_client_enrollments(db: Session, client_id: int):
        """Helper method to get enrollments for a client"""
        return db.query(
            Enrollment.program_id,
            Program.name.label("program_name"),
            Enrollment.enrollment_date
        ).join(
            Program, Enrollment.program_id == Program.id
        ).filter(
            Enrollment.client_id == client_id
        ).all()
    
    @staticmethod
    def _create_program_enrollments(enrollments):
        """Helper method to create program enrollment objects"""
        return [
            ProgramEnrollment(
                program_id=enrollment.program_id,
                program_name=enrollment.program_name,
                enrollment_date=enrollment.enrollment_date
            )
            for enrollment in enrollments
        ]
    
    @staticmethod
    def _client_to_dict(client, enrollments):
        """Helper method to convert client and enrollments to a dictionary"""
        client_data = {
            "id": client.id,
            "name": client.name, 
            "date_of_birth": client.date_of_birth,
            "contact_info": client.contact_info,
            "gender": client.gender.value if client.gender else None,
            "enrollments": enrollments
        }
        return client_data
    
    @staticmethod
    def _process_clients_with_enrollments(db: Session, clients):
        """Helper method to process clients and add their enrollments"""
        result = []
        for client in clients:
            # Get enrollments for the client
            enrollments = ClientService._get_client_enrollments(db, client.id)
            
            # Convert to program enrollment objects
            program_enrollments = ClientService._create_program_enrollments(enrollments)
            
            # Create client data with enrollments
            client_data = ClientService._client_to_dict(client, program_enrollments)
            
            # Add to results
            result.append(client_data)
        
        return result
    
    @staticmethod
    def get_clients(db: Session, skip: int = 0, limit: int = 100):
        """Get all clients with their enrollments"""
        clients = db.query(Client).offset(skip).limit(limit).all()
        return ClientService._process_clients_with_enrollments(db, clients)
    
    @staticmethod
    def search_clients(db: Session, search: str, skip: int = 0, limit: int = 100):
        """Search clients by name or contact info"""
        clients = db.query(Client).filter(
            or_(
                Client.name.ilike(f"%{search}%"),
                Client.contact_info.ilike(f"%{search}%")
            )
        ).offset(skip).limit(limit).all()
        
        return ClientService._process_clients_with_enrollments(db, clients)
    
    @staticmethod
    def get_client_by_id(db: Session, client_id: int):
        """Get a client by ID"""
        return db.query(Client).filter(Client.id == client_id).first()
    
    @staticmethod
    def verify_client_exists(db: Session, client_id: int):
        """Verify that a client exists and return it or raise a ValueError"""
        client = ClientService.get_client_by_id(db, client_id)
        if not client:
            raise ValueError(f"Client with ID {client_id} not found")
        return client
    
    @staticmethod
    def get_client_profile(db: Session, client_id: int):
        """Get a client profile with their program enrollments"""
        db_client = ClientService.get_client_by_id(db, client_id)
        
        if db_client is None:
            return None
            
        # Get enrollments with program information
        enrollments = ClientService._get_client_enrollments(db, client_id)
        
        # Create program enrollments
        program_enrollments = ClientService._create_program_enrollments(enrollments)
        
        # Create the ClientProfile response model
        return ClientProfile(
            id=db_client.id,
            name=db_client.name,
            date_of_birth=db_client.date_of_birth,
            contact_info=db_client.contact_info,
            gender=db_client.gender.value if db_client.gender else None,
            enrollments=program_enrollments
        )


class EnrollmentService:
    @staticmethod
    def enroll_client(db: Session, client_id: int, enrollment: EnrollmentCreate):
        """Enroll a client in a health program"""
        # Verify client and program exist
        client = ClientService.verify_client_exists(db, client_id)
        program = ProgramService.verify_program_exists(db, enrollment.program_id)
        
        # Create enrollment
        db_enrollment = Enrollment(
            client_id=client_id,
            program_id=enrollment.program_id,
            enrollment_date=enrollment.enrollment_date if enrollment.enrollment_date else date.today()
        )
        
        try:
            db.add(db_enrollment)
            db.commit()
            db.refresh(db_enrollment)
            
            # Ensure the program relationship is loaded
            db.refresh(db_enrollment.program)
            
            return db_enrollment
        except IntegrityError:
            db.rollback()
            raise ValueError(f"Client {client_id} is already enrolled in program {enrollment.program_id}")
    
    @staticmethod
    def get_client_enrollments(db: Session, client_id: int):
        """Get all enrollments for a client"""
        # Verify client exists
        ClientService.verify_client_exists(db, client_id)
        return db.query(Enrollment).filter(Enrollment.client_id == client_id).all() 