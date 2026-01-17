# HBnB – Database Integration and Persistence

This project represents **Part 3** of the HBnB (Holberton Bed & Breakfast) application.  
In this phase, the system transitions from **in-memory data storage** to a **database-backed persistence layer** using a relational database.

The primary goal of this part is to introduce permanent data storage while preserving the existing API behavior and maintaining a clean, scalable architecture.

---

## Objectives

The objectives of this phase are to:

- Replace in-memory persistence with database storage
- Integrate SQLAlchemy as the Object Relational Mapper (ORM)
- Implement proper session and transaction management
- Maintain clear separation between application layers
- Ensure data consistency and long-term persistence

---

## Architecture 

The application follows a layered architecture with clear responsibility boundaries:

```
Client
↓
API Layer (Flask / Flask-RESTX)
↓
Business Logic Layer (Facade Pattern)
↓
Persistence Layer (SQLAlchemy + Relational Database)
```


This structure improves maintainability, scalability, and testability.

---

## Project Structure (Part 3 – Actual Implementation)

The following directory structure reflects the **actual file layout used in Part 3**,
based strictly on the implemented project files.

```
part3/
└── hbnb/
    ├── app/
    │   │
    │   ├── api/
    │   │   ├── __init__.py
    │   │
    │   │   └── v1/
    │   │       ├── __init__.py
    │   │       ├── users.py
    │   │       ├── places.py
    │   │       ├── review.py
    │   │       ├── amenities.py
    │   │       └── auth.py
    │   │
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── base_model.py
    │   │   ├── user.py
    │   │   ├── place.py
    │   │   ├── amenity.py
    │   │   ├── review.py
    │   │   └── validation.py
    │   │
    │   ├── repositories/
    │   │   ├── __init__.py
    │   │   ├── in_memory_repository.py
    │   │   └── sqlalchemy_repository.py
    │   │
    │   ├── services/
    │   │   ├── __init__.py
    │   │   └── facade.py
    │   └── __init__.py
    │   │
    ├── sql/
    │   ├── create_tables.sql
    │   └── insert_admin.sql
    │
    ├── run.py
    ├── config.py
    ├── requirements.txt
    ├── README.md
    ├── simple_test_report.md
    ├── test_models.py
    ├── test_users.sh
    └── test_amenities_places.sh

```
---
## SQL and Database Files

### - `repositories/sqlalchemy_repository.py`
Handles database operations using SQLAlchemy.
It is responsible for saving, retrieving, and updating data in the database,
replacing in-memory storage with persistent SQL-based storage.

### - `api/v1/auth.py`
Manages authentication-related API endpoints.
It verifies user credentials using stored database data and prepares
the application for secure access.

### - `sql/create_tables.sql`
Contains SQL statements used to create the database tables
and define the schema structure.

### - `sql/insert_admin.sql`
Provides initial SQL data for the database,
such as inserting a default or administrative user.

### - Database Integration (`db`)
The database layer is responsible for establishing the connection,
managing sessions, and ensuring data is stored persistently.
It acts as the foundation that links the application logic
with the SQL database.

---

## Testing
*The project can be tested using:*

- Manual API testing with `curl`
- Automated test scripts located in the `tests/` directory

**Example request:**
```
curl -X POST http://127.0.0.1:5000/api/v1/users \
-H "Content-Type: application/json" \
-d '{"email":"test@mail.com","password":"1234"}'
```

## How to Run the Project

1- **Install dependencies:**
```
pip install -r requirements.txt
```
2- **Initialize the database:**
```
python3 -m app.persistence.db
```

3- **Start the application:**
```
python3 run.py
```

4- **Access the API:**
```
http://127.0.0.1:5000/api/v1/
```
---
### Key Improvements from Part 2

- Introduction of database-backed persistence
- SQLAlchemy ORM integration
- Improved separation of concerns
- Enhanced scalability and maintainability
---
