from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, UniqueConstraint, func, Enum
from sqlalchemy.orm import relationship, joinedload
from datetime import date, datetime
import enum

from ..database.database import Base

class Gender(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    contact_info = Column(String, nullable=True)
    gender = Column(Enum(Gender), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with Enrollment
    enrollments = relationship("Enrollment", back_populates="client", cascade="all, delete-orphan")

class Program(Base):
    __tablename__ = "programs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with Enrollment
    enrollments = relationship("Enrollment", back_populates="program", cascade="all, delete-orphan")

class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    program_id = Column(Integer, ForeignKey("programs.id", ondelete="CASCADE"), nullable=False)
    enrollment_date = Column(Date, default=date.today, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="enrollments")
    program = relationship("Program", back_populates="enrollments", lazy="joined")
    
    # Ensure a client can only be enrolled once per program
    __table_args__ = (
        UniqueConstraint('client_id', 'program_id', name='uq_client_program'),
    ) 