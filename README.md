# Social Network API

This project is a Django-based REST API for a simple social networking application.

## Features

- User registration and authentication
- User search functionality
- Friend request system
- List friends and pending friend requests

## Installation

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (for containerized setup)

### Local Setup

1. Clone the repository:
   ```
   git clone https://github.com/akashkumar19/social-network-api.git
   cd social-network-api
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Start the development server:
   ```
   python manage.py runserver
   ```

### Docker Setup

1. Clone the repository:
   ```
   git clone https://github.com/akashkumar19/social-network-api.git
   cd social-network-api
   ```

2. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

The API will be available at `http://localhost:8000`.

## API Documentation

Please refer to the Postman collection in the `postman` directory for detailed API documentation and example requests.

