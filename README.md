# Holbertonschool-Hbnb Project

HBnB Evolution is a technical documentation project focused on designing the architecture of a simplified Airbnb-like application.  
The objective of this project is to define a clear system structure using a layered architecture approach before moving into the implementation phase.  
This documentation serves as a foundational blueprint that explains how different components of the system are organized and how they interact with each other.  
Emphasis is placed on UML modeling, clean architectural design, and separation of concerns.

---
# Part 1 – System Architecture and Design

## Package Diagram

This section presents the High-Level Package Diagram for the HBnB Evolution application.  
The diagram illustrates the overall system architecture based on a three-layer structure: Presentation Layer, Business Logic Layer, and Persistence Layer.  
It highlights how the layers interact with each other through the Facade Pattern, providing a clear separation of concerns and simplifying communication between components.  
This diagram offers a conceptual overview of the system without including implementation or database-specific details.

<img src="part1/hbnb_package_diagram.png" width="200">

---

## Class Diagram

This section documents the class diagram for the Business Logic layer of the HBnB application.  
The diagram describes the core domain entities, their attributes, methods, and the relationships that govern their interactions.  
It focuses on modeling the fundamental business rules and behaviors independently of presentation or persistence concerns, ensuring a clean and maintainable design.

<img src="part1/Hbnb_Class_Diagram.png" width="1000">

---

## Sequence Diagrams

This section presents the sequence diagrams for the HBnB Evolution application.  
These diagrams illustrate how the Presentation Layer, Business Logic Layer, and Persistence Layer interact to handle key user operations.  
Each sequence diagram represents a specific API use case and demonstrates the flow of requests and responses across the system layers, highlighting how business logic is processed and how data is stored or retrieved.


<p align="left">
<img src="part1/Sequence Diagrams User Registration.png" width="450">
<img src="part1/Sequence Diagrams Place Creation.png" width="450">
<img src="part1/Sequence Diagrams Review Submission.png" width="450">
<img src="part1/Sequence Diagrams Fetching a List of Place.png" width="450">
</p>

--- 

# Part 2 – Business Logic and API Implementation

This part of the **HBnB** project focuses on implementing the **Business Logic Layer (BL)** and exposing application functionality through **RESTful API endpoints**.  
The implementation follows the architecture previously defined and applies the **Facade Design Pattern** to centralize business operations and enforce a clean separation between layers.

An **in-memory persistence mechanism** is used to manage entities and apply business rules such as data validation and entity relationships.  
This stage delivers a functional and maintainable backend foundation.

---

## Business Logic Overview

The Business Logic Layer is responsible for validating input data, enforcing business rules, coordinating interactions between the API and repository layers, and preventing invalid operations such as creating entities with non-existent relationships.

All business behavior is centralized to ensure consistent and reliable application behavior regardless of how the API is accessed.

---

## Architecture and Design

The application follows a layered architecture consisting of:
- An API Layer for handling HTTP requests and responses
- A Business Logic Layer for validation and rule enforcement
- A Repository Layer for abstracting data storage

All communication between layers is coordinated through the **Facade**, improving maintainability, scalability, and testability.

---

## Persistence Strategy

Data persistence in this phase is simulated using in-memory Python data structures.  
This approach allows the application to focus on enforcing business logic, validation rules, and entity relationships without introducing database complexity.

All stored data is reset when the server restarts, which is an intentional design choice aligned with the scope of this project stage.  
This strategy supports rapid development, easier debugging, and clear validation of application behavior before integrating permanent storage solutions in future phases.

---

## API Implementation

RESTful API endpoints are implemented using **Flask** and **Flask-RESTX**, providing a clean and structured interface for interacting with the application.  
The API enables operations on core entities such as Users, Places, Amenities, and Reviews using standard HTTP methods and JSON payloads.

Flask-RESTX is also used to automatically generate **Swagger documentation**, offering an interactive view of available endpoints, request formats, and response structures.  
This improves usability, consistency, and clarity for both development and testing.

---

## Testing and Validation

API functionality is validated using automated shell scripts that simulate real client requests through the `curl` command-line tool.  
These scripts are designed to test both successful and invalid scenarios to ensure correct behavior under different conditions.

- `test_users.sh` validates **Tasks 1–3**, covering user creation, retrieval, and update operations.
- `test_amenities_places.sh` validates **Tasks 4–6**, covering amenity operations and place creation with owner validation.

Testing verifies:
- Correct enforcement of business rules
- Proper handling of invalid input and non-existent resources
- Accurate HTTP status codes
- Consistent and structured JSON responses

---

## Summary

Part 2 delivers a functional backend implementation that transforms architectural design into executable code.  
By centralizing business logic through the Facade Pattern, enforcing validation rules, exposing RESTful APIs, and validating behavior through structured testing, this stage provides a solid and maintainable foundation for future enhancements such as persistent storage and authentication.

---
## Authors

### Shaden Majed Alalwani  
Riyadh, Saudi Arabia  
Student at Holberton Schools  
GitHub: https://github.com/Shadenm-404  

### Nada Ghannam Al-Mutairi  
Riyadh, Saudi Arabia  
Student at Holberton Schools  
GitHub: https://github.com/NadaGhannam25  

### Sondos Saleh Alrubaish  
Riyadh, Saudi Arabia  
Student at Holberton Schools  
GitHub: https://github.com/sondos04  



