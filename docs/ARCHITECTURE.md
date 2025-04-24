# System Architecture

This document describes the proposed architecture for the Basic Health Information System (BHIS) Prototype.

## 1. Overview

The system will be developed as a monolithic web application with a RESTful API.

*   **Monolithic Approach:** For simplicity in this prototype, all core functionalities (client management, program management, enrollments, API) will reside within a single application codebase.
*   **API-Centric:** While potentially having a simple UI for demonstration, the core logic will be accessible via a well-defined REST API, fulfilling requirement #6 and aligning with the "API first approach" suggestion.

## 2. Components

*   **Web Server/Application Framework:** Handles incoming HTTP requests (API calls, potentially UI requests), routes them to appropriate handlers, and manages the request/response lifecycle. (e.g., Flask, FastAPI, Express).
*   **API Endpoints:** Specific handlers for each API operation defined in `API.md`.
*   **Business Logic Layer:** Contains the core logic for managing clients, programs, and enrollments. Enforces validation rules.
*   **Data Access Layer (DAL):** Responsible for interacting with the chosen database. Abstracts database operations from the business logic. (e.g., using an ORM like SQLAlchemy or Sequelize, or direct DB queries).
*   **Database:** Stores all persistent data, including client information, program details, and enrollment records. (e.g., SQLite for simplicity, PostgreSQL for more features).

## 3. Technology Choices (Preliminary)

*   **Language/Framework:** [TBD - Choice depends on developer familiarity. Python/Flask or Python/FastAPI are strong contenders due to simplicity and rapid development. Node.js/Express is another option.]
*   **Database:** [TBD - SQLite is suitable for a simple prototype. If scalability or more complex queries are anticipated later, PostgreSQL would be a better choice.]
*   **API Specification:** OpenAPI (Swagger) could be used to formally define and document the API, potentially auto-generating documentation.

## 4. Data Flow (Example: Registering a Client via API)

1.  **External System/UI:** Sends a `POST` request to `/api/clients` with client data in the request body (JSON).
2.  **Web Server:** Receives the request.
3.  **Routing:** Directs the request to the "Register Client" API endpoint handler.
4.  **API Endpoint Handler:** Parses and validates the incoming JSON data.
5.  **Business Logic:** Performs any necessary checks (e.g., ensure required fields are present).
6.  **Data Access Layer:** Constructs a database command to insert the new client record.
7.  **Database:** Executes the command and persists the new client data.
8.  **Response:** The API handler formats a success response (e.g., `201 Created` with the new client's ID and URI) and sends it back through the Web Server to the caller.

## 5. Considerations

*   **Scalability:** The monolithic approach is simple but may face scalability challenges long-term. For a prototype, this is acceptable.
*   **Testing:** The separation into layers (API, Business Logic, DAL) facilitates unit testing.
*   **Security:** API endpoints will need protection (details TBD - potentially simple API keys for the prototype). 