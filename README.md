# CEMA BHIS - My Health Information System Project 🏥

I built this lightweight health information system to help healthcare providers manage their clients and health programs effectively. It streamlines workflows while keeping everything secure and user-friendly.

## 💡 What I Created

CEMA BHIS (Basic Health Information System) is a solution I developed to tackle healthcare data management challenges. I wanted to create something practical for real-world use while demonstrating clean code principles and an API-first approach.

## 🔑 Key Features

The system allows healthcare workers to:

1. **🆕 Create health programs** - Set up specialized care programs (TB, Malaria, HIV, etc.)
2. **👤 Register clients** - Add and manage patient information seamlessly
3. **📋 Enroll clients in programs** - Connect patients with the care they need
4. **🔍 Search for clients** - Find patients quickly with a robust search system
5. **👁️ View client profiles** - See comprehensive patient information including program enrollment
6. **🔌 Access data via API** - Secure API layer for external system integration

## 🏗️ Project Structure

I organized the project with a clear separation of concerns:

```
CEMA BHIS/
├── README.md            # Project overview
├── backend/             # Python backend implementation
│   ├── .env             # Environment configuration
│   ├── bhis.db          # SQLite database
│   ├── docs/            # Documentation
│   ├── requirements.txt # Dependencies
│   ├── run.py           # Entry point
│   ├── scripts/         # Helper scripts
│   └── src/             # Backend source code
└── frontend/            # React.js frontend
    ├── public/          # Static assets
    ├── src/             # Frontend source
    ├── package.json     # Dependencies and scripts
    └── README.md        # Frontend-specific notes
```

## 💻 Technology Choices

- **Backend**: Python with FastAPI for performance and simplicity
- **Database**: SQLite for development (easily scalable to PostgreSQL in production)
- **API**: RESTful design with JSON responses and security features
- **Frontend**: React.js with Material-UI for a modern, responsive interface

## 🚀 How to Run It

### Backend Setup

1. **Prerequisites:**
   - Python 3.8+
   - pip

2. **Installing dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Database setup:**
   I configured the database in `backend/.env`:
   ```
   DATABASE_URL=sqlite:///bhis.db
   API_KEY=dev_api_key_for_testing
   ```

4. **Running the server:**
   ```bash
   cd backend
   python run.py
   ```
   - Access API documentation: http://localhost:8000/docs
   - API base URL: http://localhost:8000/

### Frontend Setup

1. **Prerequisites:**
   - Node.js 14+
   - npm or yarn

2. **Installing dependencies:**
   ```bash
   cd frontend
   npm install
   ```

3. **Running the dev server:**
   ```bash
   npm start
   ```
   - View the app: http://localhost:3000

## 🧪 Testing My Code

```bash
# Run all tests
python -m pytest tests/test_bhis.py -v

# Run specific test categories
python -m pytest tests/test_bhis.py -k "api" -v    # API tests
python -m pytest tests/test_bhis.py -k "program" -v  # Program tests
python -m pytest tests/test_bhis.py -k "client" -v   # Client tests

# Frontend tests
cd frontend
npm test
```

## 🔗 API Endpoints

I designed these endpoints to cover the core functionality:

- **Programs:**
  - `POST /programs/` - Create a program
  - `GET /programs/` - List all programs

- **Clients:**
  - `POST /clients/` - Register a client
  - `GET /clients/?search=<term>` - Search for clients
  - `GET /clients/{client_id}` - View a client profile

- **Enrollments:**
  - `POST /clients/{client_id}/enrollments/` - Enroll a client in a program

- **External API (requires authentication):**
  - `GET /api/clients/{client_id}` - Get client data securely

## 🔒 Security Implementation

- API endpoints protected with key-based authentication
- Input validation to prevent SQL injection and XSS attacks
- Data encryption for sensitive client information
- Role-based access control
- HTTPS support for secure data transmission

## 🚀 Deployment

The app can be deployed using Docker:

```bash
docker-compose up
```

## 📝 Development Approach

Throughout this project, I focused on:
- Writing clean, maintainable code
- Taking an API-first approach
- Creating an intuitive workflow for healthcare users
- Implementing robust security measures
- Building an extensible architecture

## 📜 License

This project is licensed under the MIT License.

## 📞 Contact

Feel free to reach out if you have questions about my project or development process!