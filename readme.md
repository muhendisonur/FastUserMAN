# FastUserMAN

A simple REST API for user management built with FastAPI and SQLAlchemy.

## Project Structure

```
userapi/
├── data/
│   └── user_data.db          # SQLite database file
├── src/
│   ├── config.py             # Configuration settings
│   ├── main.py               # FastAPI application entry point
│   ├── database/
│   │   ├── db_operations.py  # Database initialization
│   │   └── models.py         # SQLAlchemy models
│   ├── exceptions/
│   │   └── UserExistsError.py # Custom exception classes
│   ├── routes/
│   │   └── user_routes.py    # API route definitions
│   ├── schemas/
│   │   ├── User.py           # User schema with ID
│   │   ├── UserUpdate.py     # User update schema
│   │   └── UserWithoutID.py  # User creation schema
│   └── services/
│       └── user_service.py   # Business logic layer
├── test/
│   ├── conftest.py           # Test configuration and fixtures
│   └── test_user_routes.py   # API endpoint tests
├── requirements.txt          # Project dependencies
└── pyproject.toml           # Project metadata
```

## Features

- **Create users**: Add new users with name, email, and age
- **Get all users**: Retrieve a list of all users
- **Get user by ID**: Find a specific user by their ID
- **Update users**: Modify existing user information
- **Delete users**: Remove users from the database
- **Email validation**: Ensures unique email addresses
- **Age validation**: Users must be older than 10 years

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd userapi
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**
   ```python
   from src.database.db_operations import init_models
   init_models()
   ```

## Running the Application

1. **Start the server**
   ```bash
   uvicorn src.main:app --reload
   ```

2. **Access the API**
   - API Base URL: `http://localhost:8000`
   - Interactive Documentation: `http://localhost:8000/docs`
   - Alternative Documentation: `http://localhost:8000/redoc`

## API Endpoints

### Get All Users
- **GET** `/users/`
- **Response**: List of users or `null` if no users exist

### Get User by ID
- **GET** `/users/{user_id}`
- **Parameters**: `user_id` (integer)
- **Response**: User object or 404 if not found

### Add New User
- **POST** `/users/add`
- **Body**:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 25
  }
  ```
- **Response**: Success message or 422 if validation fails

### Update User
- **PUT** `/users/update`
- **Body**:
  ```json
  {
    "user_id": 1,
    "name": "Updated Name",
    "email": "updated@example.com",
    "age": 30
  }
  ```
- **Note**: All fields except `user_id` are optional

### Delete User
- **GET** `/users/delete/{user_id}`
- **Parameters**: `user_id` (integer)
- **Response**: Success message or 404 if user not found

## Data Validation

The API includes several validation rules:

- **Name**: Maximum 50 characters
- **Email**: Valid email format, maximum 100 characters, must be unique
- **Age**: Must be greater than 10
- **User ID**: Must be a positive integer

## Testing

Run the test suite using pytest:

```bash
pytest test/
```

The project includes:
- **Integration tests**: Test complete API workflows with real database
- **Unit tests**: Test individual components with mocked dependencies

## Configuration

Update the database path in `src/config.py`:

```python
db_path = "path/to/your/database.db"
url_prefix = "/users"
```

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type hints
- **Pytest**: Testing framework
- **SQLite**: Lightweight database engine

## Error Handling

The API handles common errors:

- **404 Not Found**: When a user doesn't exist
- **422 Unprocessable Entity**: When validation fails
- **500 Internal Server Error**: For unexpected server errors

## Custom Exceptions

- **UserExistsError**: Raised when trying to create a user with an existing email address

## Architecture

The project follows a clean architecture pattern:

1. **Routes Layer** (`routes/`): Handles HTTP requests and responses
2. **Service Layer** (`services/`): Contains business logic
3. **Data Layer** (`database/`): Manages database operations
4. **Schema Layer** (`schemas/`): Defines data validation models

This separation ensures the code is maintainable, testable, and follows best practices.
