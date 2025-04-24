# Data Model

This document outlines the proposed data structures for the BHIS prototype.

## 1. Database Choice

*   **Recommendation:** SQLite
*   **Rationale:** Simple file-based database, sufficient for a prototype, requires no separate server setup. Easy to include in the repository if needed for demonstration. Can be migrated to PostgreSQL or similar later if required.

## 2. Entities / Tables

### 2.1. `clients`

Stores information about registered clients.

| Column         | Data Type      | Constraints         | Description                                  |
|----------------|----------------|---------------------|----------------------------------------------|
| `id`           | INTEGER / UUID | PRIMARY KEY         | Unique identifier for the client             |
| `name`         | TEXT           | NOT NULL            | Full name of the client                      |
| `date_of_birth`| DATE           | NOT NULL            | Client's date of birth (YYYY-MM-DD)          |
| `contact_info` | TEXT           |                     | Optional contact details (e.g., phone, email)|
| `created_at`   | TIMESTAMP      | DEFAULT CURRENT_TIME| Timestamp when the record was created        |
| `updated_at`   | TIMESTAMP      | DEFAULT CURRENT_TIME| Timestamp when the record was last updated   |

*Note: Using an auto-incrementing INTEGER primary key is simplest for SQLite. A UUID might be better for distributed systems but adds complexity.* 

### 2.2. `programs`

Stores information about available health programs.

| Column        | Data Type      | Constraints         | Description                               |
|---------------|----------------|---------------------|-------------------------------------------|
| `id`          | INTEGER / UUID | PRIMARY KEY         | Unique identifier for the program         |
| `name`        | TEXT           | NOT NULL, UNIQUE    | Name of the health program (e.g., HIV)    |
| `description` | TEXT           |                     | Optional description of the program       |
| `created_at`  | TIMESTAMP      | DEFAULT CURRENT_TIME| Timestamp when the record was created     |
| `updated_at`  | TIMESTAMP      | DEFAULT CURRENT_TIME| Timestamp when the record was last updated|

### 2.3. `enrollments`

Represents the many-to-many relationship between clients and programs.

| Column            | Data Type      | Constraints                 | Description                                         |
|-------------------|----------------|-----------------------------|-----------------------------------------------------|
| `id`              | INTEGER / UUID | PRIMARY KEY                 | Unique identifier for the enrollment record         |
| `client_id`       | INTEGER / UUID | NOT NULL, FOREIGN KEY       | References `clients(id)`                            |
| `program_id`      | INTEGER / UUID | NOT NULL, FOREIGN KEY       | References `programs(id)`                           |
| `enrollment_date` | DATE           | NOT NULL, DEFAULT CURRENT_DATE| Date the client was enrolled in the program         |
| `created_at`      | TIMESTAMP      | DEFAULT CURRENT_TIME        | Timestamp when the record was created             |
|                   |                | UNIQUE (`client_id`, `program_id`) | Ensure a client can only enroll once per program |

## 3. Relationships

*   **Clients to Enrollments:** One-to-Many (One client can have many enrollments).
*   **Programs to Enrollments:** One-to-Many (One program can have many enrollments).
*   **Clients to Programs:** Many-to-Many (Managed via the `enrollments` table).

## 4. Considerations

*   **Indexing:** Add indexes to foreign keys (`client_id`, `program_id` in `enrollments`) and potentially `clients.name` for faster lookups.
*   **Data Types:** Specific data types might vary slightly depending on the chosen database system and ORM.
*   **Normalization:** This structure is reasonably normalized. 