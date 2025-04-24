# CEMA BHIS - Basic Health Information System 🏥

A lightweight health information system for managing clients and health programs/services, designed to streamline healthcare management workflows.

## 🌟 Project Overview

CEMA BHIS (Basic Health Information System) is a comprehensive solution that enables healthcare providers to efficiently manage patient data and health programs. This project was developed as part of a software engineering task to demonstrate clean code, API-first approach, and practical implementation of software development skills.

## 🔑 Key Features

This system allows healthcare workers (doctors/system users) to:

1. **🆕 Create health programs** - Set up health programs like TB, Malaria, HIV, etc. with specific treatment protocols and monitoring requirements
2. **👤 Register clients** - Add new patients to the system with their personal and medical information
3. **📋 Enroll clients** - Connect clients to one or more health programs for appropriate care
4. **🔍 Search for clients** - Quickly find registered clients using various search parameters
5. **👁️ View client profiles** - Access comprehensive client information including their enrolled programs
6. **🔌 Expose client data via API** - Allow external systems to securely retrieve client information

## 🏗️ Project Structure

```
CEMA BHIS/
├── README.md            # Project overview (this file)
├── backend/             # Backend code and documentation
│   ├── .env             # Environment configuration
│   ├── bhis.db          # SQLite database
│   ├── docs/            # Documentation files
│   ├── requirements.txt # Python dependencies
│   ├── run.py           # Application entry point
│   ├── scripts/         # Utility scripts
│   └── src/             # Source code
└── frontend/            # Frontend implementation
    ├── public/          # Static assets
    ├── src/             # Frontend source code
    ├── package.json     # Dependencies and scripts
    └── README.md        # Frontend-specific documentation
```

## 💻 Technology Stack

- **Backend**: Python with FastAPI, SQLite database
- **API**: RESTful with JSON responses, security-enhanced endpoints
- **Frontend**: React.js with Material-UI, Redux for state management

## 🚀 Setup Instructions

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

### Frontend Setup

1. **Prerequisites:**
   - Node.js 14+
   - npm or yarn

2. **Install frontend dependencies:**
   ```bash
   cd frontend
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm start
   ```

4. **Access the web application:**
   - Frontend URL: http://localhost:3000

## 🧪 Running Tests

The application includes a comprehensive test suite to ensure functionality and reliability:

### Running Backend Tests

```bash
# From the project root directory
python -m pytest tests/test_bhis.py -v
```

You can also run specific test categories:
```bash
# Run only API tests
python -m pytest tests/test_bhis.py -k "api" -v

# Run only program-related tests
python -m pytest tests/test_bhis.py -k "program" -v

# Run only client-related tests
python -m pytest tests/test_bhis.py -k "client" -v
```

### Running Frontend Tests (when implemented)

```bash
cd frontend
npm test
```

## 🔄 Development Workflow

### Backend Development

1. Start the backend server:
   ```bash
   cd backend
   python run.py
   ```
   This will start the server with hot-reload enabled.

2. Access the API documentation:
   - Visit http://localhost:8000/docs to see and test available endpoints

3. Make changes to the backend code:
   - The server will automatically reload when you save changes

### Frontend Development

1. Start the frontend development server:
   ```bash
   cd frontend
   npm start
   ```

2. Open your browser:
   - Visit http://localhost:3000 to see your changes in real-time
   - The page will reload automatically when you save changes

## 🔗 API Endpoints

- **Programs:**
  - `POST /programs/` - Create a health program
  - `GET /programs/` - List all programs

- **Clients:**
  - `POST /clients/` - Register a client
  - `GET /clients/?search=<n>` - List/search clients
  - `GET /clients/{client_id}` - View client profile

- **Enrollments:**
  - `POST /clients/{client_id}/enrollments/` - Enroll client in program

- **External API (requires API key):**
  - `GET /api/clients/{client_id}` - Get client profile via API

## 🔒 Security Considerations

- API endpoints are protected with API key authentication
- User input validation to prevent SQL injection and XSS attacks
- Data encryption for sensitive client information
- Role-based access control for different user types
- HTTPS for secure data transmission

## 🚀 Deployment

This application can be deployed using Docker containers for both development and production environments:

```bash
docker-compose up
```

## 📝 What to Expect

- Clean, well-documented code
- API-first approach
- Intuitive workflow for healthcare providers
- Secure data handling
- Extensible architecture

## 🌐 Frontend Roadmap

The frontend development follows these key milestones:

1. **Phase 1 (Current):**
   - User authentication and authorization
   - Program management dashboard
   - Client registration and profile views
   - Basic search functionality

2. **Phase 2 (Upcoming):**
   - Enhanced UI/UX with responsive design
   - Advanced search with filters and sorting
   - Data visualization for program statistics
   - Batch operations for client management

3. **Phase 3 (Future):**
   - Offline capability with data synchronization
   - Mobile-optimized views
   - Real-time notifications
   - Integration with external health systems

## 📊 Future Enhancements

- Mobile application for field healthcare workers
- Advanced reporting and analytics
- Integration with electronic medical record systems
- Offline capability for remote areas with limited connectivity
- AI-assisted diagnosis and treatment recommendations

## 🔄 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

For questions or support, please contact the CEMA BHIS team at support@cemabhis.example.com