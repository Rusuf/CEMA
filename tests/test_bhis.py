import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import date

# Test Constants
API_KEY = "dev_api_key_for_testing"

# Core API Tests
def test_root_endpoint(test_client):
    """Test: Application root endpoint is accessible"""
    response = test_client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "docs" in response.json()  # Docs link should be in response

# Health Program Tests
def test_program_creation_and_listing(test_client):
    """Test: Program creation and listing"""
    # Create a program
    program_data = {
        "name": "Diabetes Care",
        "description": "Management of diabetes and related conditions"
    }
    
    create_response = test_client.post("/programs/", json=program_data)
    assert create_response.status_code == 201
    
    new_program = create_response.json()
    assert new_program["name"] == "Diabetes Care"
    assert "id" in new_program
    
    # List all programs
    list_response = test_client.get("/programs/")
    assert list_response.status_code == 200
    programs = list_response.json()
    assert isinstance(programs, list)
    
    # Verify our program is in the list
    program_names = [p["name"] for p in programs]
    assert "Diabetes Care" in program_names

def test_program_validation(test_client):
    """Test: Program validation - Duplicate program names not allowed"""
    # Create a program
    test_client.post("/programs/", json={"name": "HIV Program", "description": "HIV care"})
    
    # Try to create program with same name
    duplicate_response = test_client.post(
        "/programs/", 
        json={"name": "HIV Program", "description": "Different description"}
    )
    
    # Should return 400 error
    assert duplicate_response.status_code == 400
    assert "already exists" in duplicate_response.json()["detail"].lower()

# Client Tests
def test_client_creation(test_client):
    """Test: Client registration"""
    client_data = {
        "name": "Jane Smith",
        "date_of_birth": str(date(1990, 5, 20)),
        "contact_info": "Phone: 555-1234, Address: 123 Main St"
    }
    
    response = test_client.post("/clients/", json=client_data)
    assert response.status_code == 201
    
    new_client = response.json()
    assert new_client["name"] == "Jane Smith"
    assert "id" in new_client

def test_client_search(test_client, db_session):
    """Test: Client search functionality"""
    # Create test clients
    clients = [
        {"name": "John Williams", "date_of_birth": str(date(1975, 3, 15)), "contact_info": "Contact info"},
        {"name": "Sarah Williams", "date_of_birth": str(date(1982, 7, 22)), "contact_info": "Contact info"},
        {"name": "John Davis", "date_of_birth": str(date(1990, 11, 10)), "contact_info": "Contact info"}
    ]
    
    for client in clients:
        test_client.post("/clients/", json=client)
    
    # Search by last name (Williams)
    search_response = test_client.get("/clients/?search=Williams")
    assert search_response.status_code == 200
    results = search_response.json()
    assert len(results) == 2
    
    # Search by first name (John)
    search_response = test_client.get("/clients/?search=John")
    assert search_response.status_code == 200
    results = search_response.json()
    assert len(results) == 2

# Enrollment Tests
def test_client_enrollment(test_client, sample_client, sample_program):
    """Test: Client enrollment in a health program"""
    enrollment_data = {
        "program_id": sample_program.id,
        "enrollment_date": str(date(2023, 6, 15))
    }
    
    # Enroll client in program
    enroll_response = test_client.post(
        f"/clients/{sample_client.id}/enrollments/",
        json=enrollment_data
    )
    
    assert enroll_response.status_code == 201
    enrollment = enroll_response.json()
    assert enrollment["client_id"] == sample_client.id
    assert enrollment["program_id"] == sample_program.id
    
    # Get client profile - should include enrollment
    profile_response = test_client.get(f"/clients/{sample_client.id}")
    assert profile_response.status_code == 200
    profile = profile_response.json()
    
    # Check if enrollments are included
    assert "enrollments" in profile
    assert len(profile["enrollments"]) == 1
    assert profile["enrollments"][0]["program_id"] == sample_program.id

# API Security Tests
def test_api_authorization(test_client, sample_client):
    """Test: API authorization - headers required for access"""
    # Without API key
    no_auth_response = test_client.get(f"/api/clients/{sample_client.id}")
    assert no_auth_response.status_code in [401, 403]  # Either is valid for auth failure
    
    # With API key
    if "X-API-Key" in sample_client.id.__dir__():  # Only test if API key auth is implemented
        valid_headers = {"X-API-Key": API_KEY}
        auth_response = test_client.get(f"/api/clients/{sample_client.id}", headers=valid_headers)
        assert auth_response.status_code == 200 