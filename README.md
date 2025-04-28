# 🏥 CEMA - Basic Health Information System

✨ A lightweight health information system for managing clients and health programs/services. Designed to streamline healthcare workflows while maintaining data security and usability.

## 📂 Project Structure

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

## ✅ Key Features

This system allows healthcare workers to:

1. 🆕 **Create health programs** (TB, Malaria, HIV, etc.) - Set up specialized care programs with custom attributes
2. 👤 **Register clients** into the system - Capture essential demographic and health information
3. 📋 **Enroll clients** in one or more health programs - Track participation across multiple health initiatives
4. 🔍 **Search for clients** from the registered list - Find patients quickly with powerful search functionality
5. 👁️ **View client profiles** including enrolled programs - Comprehensive patient information in one place
6. 🔌 **Access client data via API** for external system integration - Secure data sharing with authorized systems

## 💻 Technology Stack

- 🐍 **Backend**: Python with FastAPI, SQLite database (easily scalable to PostgreSQL)
- 🌐 **API**: RESTful with JSON responses, key-based authentication
- 🖥️ **Frontend**: To be implemented (planned with React.js)
- 🔒 **Security**: Input validation, data encryption for sensitive information

## 🚀 Setup Instructions

### 🔧 Backend Setup

1. **Prerequisites:**
   - Python 3.8+ 🐍
   - pip 📦

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
   - 📚 API documentation: http://localhost:8000/docs
   - 🔗 API base URL: http://localhost:8000/

### 🖥️ Frontend Setup

1. **Prerequisites:**
   - Node.js v14+ (https://nodejs.org/)

2. **Install frontend dependencies:**
   ```bash
   cd frontend
   npm install
   ```

3. **Run the frontend app:**
   ```bash
   npm start
   ```

4. **Access the frontend:**
   - 🌐 http://localhost:3000

> ⚠️ The backend server should be running at http://localhost:8000 for full functionality.

## 🧪 Testing

```bash
# Run all tests ✅
python -m pytest tests/test_bhis.py -v

# Run specific test categories
python -m pytest tests/test_bhis.py -k "api" -v    # 🌐 API tests
python -m pytest tests/test_bhis.py -k "program" -v  # 📋 Program tests
python -m pytest tests/test_bhis.py -k "client" -v   # 👤 Client tests
```

## 🔗 API Endpoints

- 📋 **Programs:**
  - `POST /programs/` - Create a health program
  - `GET /programs/` - List all programs

- 👤 **Clients:**
  - `POST /clients/` - Register a client
  - `GET /clients/?search=<name>` - List/search clients
  - `GET /clients/{client_id}` - View client profile

- 📝 **Enrollments:**
  - `POST /clients/{client_id}/enrollments/` - Enroll client in program

- 🔑 **External API (requires API key):**
  - `GET /api/clients/{client_id}` - Get client profile via API

## 🔒 Security Implementation

- 🔐 API endpoints protected with key-based authentication
- ⚔️ Input validation to prevent SQL injection and other attacks
- 🛡️ Designed with data privacy considerations for healthcare information
- 👮 Role-based access control for different user types

## 📞 Contact Information

For questions or collaboration on this project:

- 📧 Email: mathwaquerufus@gmail.com
- 📱 Phone: +254758503824

---

⭐ *Developed with care for healthcare professionals and their clients* ⭐