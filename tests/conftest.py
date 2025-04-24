import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import sys
import os
from datetime import date

# Add the parent directory to the path so we can import from backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the FastAPI app and database models
from backend.app.main import app
from backend.app.database.database import Base, get_db
from backend.app.models.models import Program, Client, Enrollment

# Configure test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Create test engine with in-memory database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite
    poolclass=StaticPool,  # Use StaticPool for in-memory testing
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create tables before tests and drop after"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Provide a test database session that rolls back changes after each test"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def override_get_db_dependency(db_session: Session):
    """Override the get_db dependency with our test database session"""
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass  # Session managed by fixture
    app.dependency_overrides[get_db] = _override_get_db
    yield
    # Clean up override after test
    del app.dependency_overrides[get_db]

@pytest.fixture(scope="function")
def test_client(override_get_db_dependency):
    """Provide a test client with test database"""
    return TestClient(app)

@pytest.fixture(scope="function")
def sample_program(db_session: Session):
    """Create a sample health program for testing"""
    program = Program(name="TB Program", description="Tuberculosis treatment program")
    db_session.add(program)
    db_session.commit()
    db_session.refresh(program)
    return program

@pytest.fixture(scope="function")
def sample_client(db_session: Session):
    """Create a sample client for testing"""
    client = Client(
        name="John Doe",
        date_of_birth=date(1985, 1, 15),
        contact_info="Phone: 1234567890, Address: 123 Test Street"
    )
    db_session.add(client)
    db_session.commit()
    db_session.refresh(client)
    return client

@pytest.fixture(scope="function")
def valid_api_key():
    """Provide a valid API key for testing"""
    return "dev_api_key_for_testing"

@pytest.fixture(scope="function")
def invalid_api_key():
    """Provide an invalid API key for testing"""
    return "invalid_api_key"

@pytest.fixture(scope="function")
def sample_enrollment(db_session: Session, sample_client: Client, sample_program: Program):
    """Create a sample enrollment for testing"""
    enrollment = Enrollment(
        client_id=sample_client.id,
        program_id=sample_program.id,
        enrollment_date=date(2023, 1, 15)
    )
    db_session.add(enrollment)
    db_session.commit()
    db_session.refresh(enrollment)
    return enrollment 