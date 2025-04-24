# CEMA - Basic Health Information System

A lightweight health information system for managing clients and health programs/services.

## Project Structure

```
CEMA/
├── README.md            # Project overview (this file)
├── backend/             # Backend code and documentation
│   ├── .env             # Environment configuration
│   ├── bhis.db          # SQLite database
│   ├── docs/            # Documentation files
│   ├── requirements.txt # Python dependencies
│   ├── run.py           # Application entry point
│   ├── scripts/         # Utility scripts
│   └── src/             # Source code
└── frontend/            # Frontend code (to be implemented)
```

## Features

This system allows healthcare workers to:

1. **Create health programs** (TB, Malaria, HIV, etc.)
2. **Register clients** into the system
3. **Enroll clients** in one or more health programs
4. **Search for clients** from the registered list
5. **View client profiles** including enrolled programs
6. **Access client data via API** for external system integration

## Technology Stack

- **Backend**: Python with FastAPI, SQLite database
- **API**: RESTful with JSON responses
- **Frontend**: To be implemented

## Setup Instructions

### Backend Setup

1. **Prerequisites:**
   - Python 3.8+
   - pip

2. **Install backend dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Database configuration:**
   The database configuration is in `backend/.env`:
   ```
   DATABASE_URL=sqlite:///bhis.db
   API_KEY=dev_api_key_for_testing
   ```

4. **Run the application:**
   ```bash
   cd backend
   python run.py
   ```

5. **Access the API:**
   - API documentation: http://localhost:8000/docs
   - API base URL: http://localhost:8000/

## API Endpoints

- **Programs:**
  - `POST /programs/` - Create a health program
  - `GET /programs/` - List all programs

- **Clients:**
  - `POST /clients/` - Register a client
  - `GET /clients/?search=<name>` - List/search clients
  - `GET /clients/{client_id}` - View client profile

- **Enrollments:**
  - `POST /clients/{client_id}/enrollments/` - Enroll client in program

- **External API (requires API key):**
  - `GET /api/clients/{client_id}` - Get client profile via API