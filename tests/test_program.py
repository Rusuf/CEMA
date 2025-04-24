import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from src.app.main import app
from src.app.database.database import Base, get_db
from src.app.models.models import Program, Client, Enrollment

# Configure test database URL (in-memory SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Create test engine and session
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}, # Required for SQLite
    poolclass=StaticPool, # Use StaticPool for in-memory testing
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture to create tables before tests and drop after
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Fixture to provide a test database session
@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

# Fixture to override the get_db dependency
@pytest.fixture(scope="function")
def override_get_db_dependency(db_session: Session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass # Session managed by fixture
    app.dependency_overrides[get_db] = _override_get_db
    yield
    # Clean up override after test
    del app.dependency_overrides[get_db]

# Fixture for the TestClient
@pytest.fixture(scope="function")
def test_client(override_get_db_dependency):
    return TestClient(app)

# --- Test Cases --- 

def test_create_program(test_client: TestClient):
    """Test creating a health program"""
    response = test_client.post(
        "/programs/",
        json={"name": "Test Program", "description": "Test Description"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Program"
    assert data["description"] == "Test Description"
    assert "id" in data

def test_create_program_duplicate(test_client: TestClient):
    """Test creating a duplicate program name"""
    test_client.post(
        "/programs/",
        json={"name": "Unique Program", "description": "Initial"}
    )
    response = test_client.post(
        "/programs/",
        json={"name": "Unique Program", "description": "Duplicate Attempt"}
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_get_programs(test_client: TestClient, db_session: Session):
    """Test retrieving health programs"""
    # Create test programs directly in the DB for this test
    program1 = Program(name="TB Care", description="TB Treatment Program")
    program2 = Program(name="HIV Support", description="Support for HIV Patients")
    db_session.add_all([program1, program2])
    db_session.commit()
    
    response = test_client.get("/programs/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2 # Check if at least the two created programs are returned
    program_names = [p["name"] for p in data]
    assert "TB Care" in program_names
    assert "HIV Support" in program_names 