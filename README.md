# Workout Tracker API - FastAPI

## Overview

This project implements a **Workout Tracker API** using **FastAPI**, which allows users to:

- Sign up and log in to manage their workouts.
- JWT-based authentication for secure access.
- CRUD operations on workout plans.
- Schedule workouts and generate progress reports.

## Features

- **User Authentication**: JWT-based authentication for secure login and signup.
- **Workout Management**: Users can create, update, delete, and schedule workouts.
- **Exercise Data**: Predefined exercises to be used in workout plans.
- **List and Manage Workouts**: List workouts based on the user, sorted by date.
- **Report Generation**: Track and generate workout reports.

## Tech Stack

- **FastAPI**: Web framework for building APIs.
- **SQLite**: Relational database used for data storage.
- **SQLAlchemy**: ORM for database interaction.
- **JWT (JSON Web Tokens)**: Secure authentication and authorization.
- **Pydantic**: Data validation for request and response bodies.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/GabriellaFGuerra/workout-tracker-api.git
cd workout-tracker-api
```

### 2. Set up a virtual environment
```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
uvicorn main:app --reload
```
The app will be running at ```127.0.0.1:8000```.	

## API Endpoints

### 1. Sign Up - /signup (POST)
#### Allows users to create an account.

- Request Body:
```json
{
  "username": "your_username",
  "email": "your_email",
  "password": "your_password"
}
```
- Response:
```json
{
  "access_token": "jwt_token",
  "token_type": "bearer"
}
```

### 2. Login - /login (POST)
Authenticate users and return a JWT token.

- Request Body (Form Data):
```json
{
  "username": "your_username",
  "password": "your_password"
}
```
- Response:
```json
{
  "access_token": "jwt_token",
  "token_type": "bearer"
}
```

### 3. Create Workout - /workouts/ (POST)
Allows authenticated users to create a workout.

- Request Body:
```json
{
  "exercise_id": 1,
  "repetitions": 10,
  "sets": 3,
  "weight": 50.0,
  "scheduled_at": "2024-09-10T14:00:00",
  "comments": "My workout comment"
}
```
- Response:
```json
{
  "message": "Workout created successfully"
}
```

### 4. List Workouts - /workouts/ (GET)
Lists all workouts for the authenticated user.

- Response:
```json
[
  {
    "id": 1,
    "exercise_id": 1,
    "repetitions": 10,
    "sets": 3,
    "weight": 50.0,
    "scheduled_at": "2024-09-10T14:00:00",
    "comments": "My workout comment"
  }
]
```

### JWT Authentication
To authenticate requests, use the token returned from the /login or /signup endpoints and include it in the Authorization header for protected routes.

```http
Authorization: Bearer <your_token>
```
### Database
This project uses SQLite as the database. The database schema is automatically created when you run the application.

- Users Table: Stores user credentials (username, email, and hashed password).

- Exercises Table: Stores predefined exercises.

- Workouts Table: Stores user workout plans.

### License
This project is licensed under the MIT License.

### Source
[Roadmap.sh](https://roadmap.sh/projects/fitness-workout-tracker)