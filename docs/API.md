# BHIS RESTful API Documentation

This document defines the REST API endpoints for the Basic Health Information System (BHIS) Prototype.

## Base URL

`[TBD - e.g., http://localhost:5000/api/v1]`

## Authentication

`[TBD - For the prototype, authentication might be omitted or use a simple static API key passed in a header (e.g., X-API-Key)]`

## Data Format

All request and response bodies will use JSON.

## Endpoints

### Health Programs

*   **`POST /programs`**: Create a new health program.
    *   Request Body:
        ```json
        {
          "name": "string (e.g., Malaria Prevention)",
          "description": "string (optional)"
        }
        ```
    *   Response: `201 Created`
        ```json
        {
          "id": "program_id",
          "name": "Malaria Prevention",
          "description": "..."
        }
        ```
*   **`GET /programs`**: Retrieve a list of all health programs.
    *   Response: `200 OK`
        ```json
        [
          {
            "id": "program_id_1",
            "name": "Program 1",
            "description": "..."
          },
          {
            "id": "program_id_2",
            "name": "Program 2",
            "description": "..."
          }
        ]
        ```

### Clients

*   **`POST /clients`**: Register a new client.
    *   Request Body:
        ```json
        {
          "name": "string",
          "date_of_birth": "YYYY-MM-DD",
          "contact_info": "string (optional)"
        }
        ```
    *   Response: `201 Created`
        ```json
        {
          "id": "client_id",
          "name": "Client Name",
          "date_of_birth": "YYYY-MM-DD",
          "contact_info": "..."
        }
        ```
*   **`GET /clients`**: Search/List registered clients.
    *   Query Parameters (Optional):
        *   `search`: string (e.g., search by name)
    *   Response: `200 OK`
        ```json
        [
          {
            "id": "client_id_1",
            "name": "Client One",
            "date_of_birth": "..."
          },
          {
            "id": "client_id_2",
            "name": "Client Two",
            "date_of_birth": "..."
          }
        ]
        ```
*   **`GET /clients/{client_id}`**: View a specific client's profile.
    *   Path Parameter: `client_id`
    *   Response: `200 OK`
        ```json
        {
          "id": "client_id",
          "name": "Client Name",
          "date_of_birth": "YYYY-MM-DD",
          "contact_info": "...",
          "enrollments": [
            {
              "program_id": "program_id_1",
              "program_name": "Program 1 Name",
              "enrollment_date": "YYYY-MM-DD"
            },
            {
              "program_id": "program_id_2",
              "program_name": "Program 2 Name",
              "enrollment_date": "YYYY-MM-DD"
            }
          ]
        }
        ```
    *   Response: `404 Not Found` if client ID doesn't exist.

### Enrollments

*   **`POST /clients/{client_id}/enrollments`**: Enroll a client in a program.
    *   Path Parameter: `client_id`
    *   Request Body:
        ```json
        {
          "program_id": "program_id_to_enroll_in"
        }
        ```
    *   Response: `201 Created`
        ```json
        {
          "enrollment_id": "new_enrollment_id",
          "client_id": "client_id",
          "program_id": "program_id",
          "enrollment_date": "YYYY-MM-DD"
        }
        ```
    *   Response: `404 Not Found` if client ID or program ID doesn't exist.
    *   Response: `400 Bad Request` if already enrolled (or other validation errors).

## Error Handling

*   `400 Bad Request`: Invalid input data or validation errors.
*   `404 Not Found`: Resource (client, program) not found.
*   `500 Internal Server Error`: Unexpected server error.

Error responses should include a descriptive message:
```json
{
  "error": "Descriptive error message"
}
``` 