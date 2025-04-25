# FastAPI Learning Project

A comprehensive learning project for FastAPI, demonstrating various aspects of building RESTful APIs with authentication, database integration, and more.

This repository is based on the Udemy course [FastAPI - The Complete Course 2025 (Beginner + Advanced)](https://www.udemy.com/course/fastapi-the-complete-course).

## Project Overview

This repository contains a series of progressive FastAPI projects:

1. **Project 1 - FastAPI Request Method Logic**: Introduction to FastAPI request methods and basic API design.
2. **Project 2 - Move Fast with FastAPI**: Building on basic concepts with more advanced patterns.
3. **Project 3 - Complete RESTful APIs**: A complete Todo application with user authentication, database persistence, and full CRUD operations.

## Project 3 Features

The most advanced project in this repository is a fully-functional Todo application with:

- User authentication with JWT tokens
- Password hashing with bcrypt
- SQLite database integration with SQLAlchemy ORM
- Complete CRUD operations for Todo items
- User-specific data isolation
- Input validation with Pydantic

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation and settings management
- **Passlib**: Password hashing library
- **Python-jose**: JWT token generation and verification
- **Uvicorn**: ASGI server for running FastAPI applications

## Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Installation

1. Clone the repository
2. Create a virtual environment (recommended):
   ```
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the Application

Navigate to the desired project directory and run:

```
uvicorn main:app --reload
```

For Project 3:

```
cd "Project 3 - Complete RESTful APIs"
uvicorn main:app --reload
```

The API will be available at http://127.0.0.1:8000.

## API Documentation

When the application is running, you can access:

- Interactive API documentation: http://127.0.0.1:8000/docs
- Alternative API documentation: http://127.0.0.1:8000/redoc

## Project Structure (Project 3)

```
Project 3 - Complete RESTful APIs/
├── database.py         # Database connection and session setup
├── main.py             # FastAPI application entry point
├── models.py           # SQLAlchemy data models
├── todos.db            # SQLite database file
└── routers/
    ├── __init__.py
    ├── auth.py         # Authentication endpoints
    └── todos.py        # Todo CRUD operations
```

## API Endpoints

### Authentication

- `POST /auth/` - Register a new user
- `POST /auth/token` - Login and get access token

### Todo Operations

- `GET /` - Get all todos for authenticated user
- `GET /todo/{todo_id}` - Get a specific todo
- `POST /todo` - Create a new todo
- `PUT /todo/{todo_id}` - Update a todo
- `DELETE /todo/{todo_id}` - Delete a todo

## License

This project is for learning purposes.

## Acknowledgements

- [FastAPI - The Complete Course](https://www.udemy.com/course/fastapi-the-complete-course) on Udemy
- FastAPI documentation and tutorials
- SQLAlchemy documentation
- Pydantic documentation
