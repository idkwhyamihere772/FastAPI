# College API (FastAPI & MongoDB)

A simple, lightweight REST API built with **FastAPI**, **MongoDB (PyMongo)**, and **Pydantic** to manage college department and student records.

## Features

- **Root Access**: Welcome message endpoint.
- **Departments Directory**: Fetch list of college departments.
- **Students Directory**: Fetch details of enrolled students.
- **Student Enrollment**: Add new students with validation using Pydantic schemas.

---

## Prerequisites

Before running the application, make sure you have the following installed:
- Python 3.8 or higher
- MongoDB (local instance or MongoDB Atlas URI)

---

## Setup & Installation

### 1. Clone the repository and switch to `dumbobranch`
```bash
git clone https://github.com/idkwhyamihere772/FastAPI.git
cd FastAPI
git checkout dumbobranch
```

### 2. Install Dependencies
Install all required libraries using `pip`:
```bash
pip install fastapi pymongo python-dotenv pydantic uvicorn
```

### 3. Environment Variables Configuration
Create a `.env` file in the root directory of the project and add your MongoDB Connection URI:
```env
mongo_uri=mongodb://localhost:27017/
```
*(Replace with your actual MongoDB URI, e.g., MongoDB Atlas connection string if hosting online.)*

---

## Running the Application

Start the FastAPI local development server using `uvicorn`:
```bash
uvicorn apidemo:app --reload
```
Once started, the API will be available at `http://127.0.0.1:8000`.

Interactive API Documentation (Swagger UI) can be accessed at: `http://127.0.0.1:8000/docs`

---

## API Endpoints Reference

### 1. Welcome Root
* **Endpoint**: `GET /`
* **Description**: Returns a simple welcome message.
* **Response**:
  ```json
  {
    "Message": "Welcome to College API"
  }
  ```

### 2. Get All Departments
* **Endpoint**: `GET /departments`
* **Description**: Fetches all departments stored in the database (`college.Department` collection).
* **Response**:
  ```json
  {
    "total": 2,
    "departments": [
      {
        "name": "Computer Science"
      },
      {
        "name": "Electrical Engineering"
      }
    ]
  }
  ```

### 3. Get All Students
* **Endpoint**: `GET /students`
* **Description**: Fetches all students stored in the database (`college.Student` collection).
* **Response**:
  ```json
  {
    "total students": 1,
    "Students": [
      {
        "name": "Jane Doe",
        "roll_no": 101,
        "course": "B.Tech CSE"
      }
    ]
  }
  ```

### 4. Add a Student
* **Endpoint**: `POST /student`
* **Description**: Registers a new student. Data is validated against the Pydantic schema before insertion.
* **Request Body**:
  ```json
  {
    "name": "Jane Doe",
    "roll_no": 101,
    "course": "B.Tech CSE"
  }
  ```
* **Response**:
  ```json
  {
    "message": "Student Added",
    "Added_Student": "Jane Doe"
  }
  ```
