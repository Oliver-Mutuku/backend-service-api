Savannah Informatics Backend Technical Challenge
This is a Python-based REST API built with Django and Django REST Framework to complete the technical challenge set by Savannah Informatics. The API manages a simple customer and orders database, handles authentication, and includes unit tests and CI/CD.

Core Technologies
Language: Python

Frameworks: Django, Django REST Framework

Database: PostgreSQL

Containerization: Docker

Authentication: OpenID Connect (via Google)

Deployment: Vercel (for the deployed API)

CI/CD: GitHub Actions

Application Features
The API fulfills the requirements of the technical challenge:




API Service: A Python service was created using Django.


Database: A simple PostgreSQL database was designed with two models: Customers (with name and code) and Orders (with item, amount, and time).



REST API: REST API endpoints were created to manage customers and orders. The endpoints are:

GET and POST requests to /api/customers/

GET and POST requests to /api/orders/


Authentication: Authentication is implemented using OpenID Connect, specifically with Google as the identity provider. The 

/api/auth/google/ endpoint verifies a Google ID token and returns JWT access and refresh tokens.

Authorization: The OrderViewSet is secured, requiring an authenticated user to create or view orders.


Automated Tests: The project includes unit tests with code coverage checks.


CI/CD: Continuous Integration (CI) and Continuous Deployment (CD) pipelines are set up using GitHub Actions to automate testing and deployment.


README: This document serves as the project's README, hosted on GitHub.

API Endpoints
The live API is deployed at http://backend-service-api.vercel.app/api/.

Authentication
POST /api/auth/google/

Description: Authenticates a user via a Google ID token.

Request Body:

JSON

{
  "id_token": "your_google_id_token_here"
}
Response:

JSON

{
  "access": "your_jwt_access_token",
  "refresh": "your_jwt_refresh_token",
  "user": {
    "id": 123,
    "email": "user@example.com",
    "username": "user"
  }
}
Customer Management
GET /api/customers/

Description: Retrieves a list of all customers.

POST /api/customers/

Description: Creates a new customer.

Request Body:

JSON

{
  "name": "John Doe",
  "code": "JD-001"
}
GET /api/customers/{id}/

Description: Retrieves details for a single customer.

Order Management
GET /api/orders/

Description: Retrieves a list of all orders. Requires authentication.

POST /api/orders/

Description: Creates a new order. Requires authentication.

Request Body:

JSON

{
  "customer": 1,
  "item": "Laptop",
  "amount": 1200.50
}
GET /api/orders/{id}/

Description: Retrieves details for a single order. Requires authentication.

Local Setup
To run this project locally, follow these steps:

Clone the repository:
```bash
    git clone https://github.com/Oliver-Mutuku/backend-service-api.git
    cd [repository directory]
    Set up environment variables:
```
Create a .env file from the .env.example template.

Configure your database connection details (e.g., PostgreSQL).

Build and run with Docker Compose:

```bash
docker-compose up --build
This command will build the Docker containers for the Django application and the PostgreSQL database, then run them. The API will be available at http://localhost:8000/.
```

Apply database migrations:
```bash
docker-compose exec web python manage.py migrate
Run tests (optional but recommended):
```
```bash
docker-compose exec web python manage.py test
```