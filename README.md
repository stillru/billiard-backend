# Billiards League Website Backend
This repository contains the backend service for the Billiards League Website. It is responsible for handling all server-side operations, including game state management, database interactions, and API endpoints for the frontend.

### Features
 - RESTful API for managing:
   - Players, matches, and teams.
   - Event logging for billiards games.
   - Match states, outcomes, and statistics.
 - Comprehensive database schema for storing all league-related data.
 - Support for dynamic match state assembly based on event logs.
 - Automated winner determination and state updates.
 - Scalable and decoupled architecture for integration with the frontend.

### Technology Stack
Framework: Flask (Python)
Database: SQLite
API Specification: OpenAPI (Swagger support)
Validation: Marshmallow
Testing: Built-in Flask test client (with TDD approach)

### Project Structure

``` shell
backend/
│
├── api/                 # API route definitions
├── app.py               # Flask application entry point
├── config.py            # Configuration settings (e.g., DB connection, API keys)
├── controllers/         # Request handlers (controllers for routing logic)
├── decorators.py        # Custom decorators (e.g., authentication, validation)
├── Dockerfile           # Docker configuration for containerization
├── extensions.py        # Third-party extensions initialization (e.g., Flask-SQLAlchemy)
├── __init__.py          # Initializes the application and registers components
├── migrations/          # Database migration scripts
├── models/              # Database models (tables, relationships)
├── populate_testing_data.py  # Script for populating sample data for testing
├── README.md            # Project documentation
├── requirements.txt     # Python dependencies
├── scheduler.py         # Background task scheduler
├── schemas/             # Validation schemas for data input/output
├── static/              # Static files (e.g., images, styles)
├── tests/               # Unit and integration tests
└── utils.py             # Helper utilities and functions
```

### Setup Instructions
Prerequisites
 - Python 3.8+
 - pip (Python package manager)

#### Installation
Clone the repository:

``` shell
git clone https://github.com/stillru/billiard-backend.git
cd billiards-league-backend
```
Create a virtual environment and activate it:

``` shell
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
Install dependencies:

``` shell
pip install -r requirements.txt
```
Initialize the database:

``` shell
flask db upgrade
```

Run the development server:

``` shell
flask run

```

### API Documentation

API endpoints are documented using OpenAPI. Once the server is running, visit the `/swagger-ui` endpoint to view the Swagger UI (e.g., http://127.0.0.1:5000/swagger-ui).

### Testing
To run the test suite:

``` shell
pytest

```
### Development Notes
The backend is designed to be frontend-agnostic, providing data exclusively in JSON format via the API.

All game state calculations are event-driven, ensuring a robust and maintainable architecture.

The SQLite database can be easily replaced with a more scalable solution (e.g., PostgreSQL) if required.

### Contributions
Contributions are welcome! Feel free to submit a pull request or open an issue to discuss improvements.

### License
This project is licensed under the MIT License. See the LICENSE file for details.
