# Business Logic Layer Documentation
This document describes the Business Logic layer of the HBnB application.
## 1. Overview
The Business Logic layer models core domain entities and business rules independently of presentation and persistence.## 2. BaseEntity Class
## 2. BaseEntity Class
**Attributes**
- id (UUID)
- created_at (DateTime)
- updated_at (DateTime)
**Methods**
- save()
- update()
- delete()
## 3. User Entity
**Methods**
- register()
- update_profile()
- delete_account()
**Relationships**
- One user can own multiple places
- One user can submit multiple reviews
## 4. Place Entity
The Place entity represents accommodation listings in the platform.
## Summary
This document provides a clear reference for implementing the HBnB Business Logic layer.
