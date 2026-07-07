# FastAPI Modular Blueprint (Router-Service-Repository Pattern)

A lightweight, well-architected FastAPI application demonstrating clean separation of concerns using the **Router-Service-Repository** pattern. This project includes fully implemented OAuth2 authentication via JWT tokens, secure password hashing, and user search features.

## 🏗️ Architecture Layout

The project enforces strict boundaries between layers to keep the codebase maintainable and testable:
- **Routers**: Handles HTTP requests, endpoint paths, and payload validation (Pydantic validation).
- **Services**: Manages the core business rules (e.g., uniqueness validation, hashing coordination).
- **Repositories**: Manages direct database access using SQLAlchemy queries.
- **Config / Models**: Handles database connection parameters and ORM infrastructure setup.

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1. Clone or Navigate to the Project
```bash
cd fastapi-blueprint
python -m venv .venv
.venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy pydantic[email] python-jose[cryptography] passlib bcrypt
uvicorn src.main:app --reload

🔑 Testing Authentication Flow via Swagger UI
1. Open your browser and navigate to the interactive docs at: http://127.0.0.1:8000/docs

2. Use the POST /users/ endpoint to register a new user account with a unique username and email.

3. Scroll to the top right of the page and click the green Authorize padlock button.

4. Enter your newly registered username and password into the OAuth2 form fields and click Authorize.

5. Once authenticated, try executing the protected GET /users/me or GET /users/ endpoints. Swagger will automatically pass your generated JWT bearer token in the headers, unlocking access.


🛠️ Main Tech Stack

FastAPI: Modern, fast web framework for building APIs.

SQLAlchemy: SQL toolkit and Object Relational Mapper (ORM) using SQLite.

Pydantic: Data validation and structural data parsing.

Python-JOSE & Passlib: Secure JWT generation and robust cryptographic validation routines.