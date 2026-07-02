# 🚗 Insait Assignment - Vehicle Info REST API Server

This project is a REST API server built with Python **FastAPI** and **SQLAlchemy** to connect to a Supabase PostgreSQL database. It is designed to query vehicle information, validate license plate patterns, and support database population using the Gemini AI model.

---

## Features

1. **REST API Endpoints**:
   - `POST /vehicle-info`: Queries the Supabase DB for a vehicle by license plate. It validates formatting rules and handles responses with correct HTTP status codes (200, 400, 404, 422, 500).
   - `GET /health`: A lightweight health check endpoint returning JSON health status.
2. **Modular Folder Layout**: Clean, scalable, production-ready directory layout separating core configs, DB models, validation schemas, routes, scripts, and tests.
3. **AI Database Loader Script**: A script that queries the Gemini API (`gemini-2.5-flash`) using structured Pydantic schemas to generate 100 unique, realistic vehicles and load them into the database safely.

---

## Directory Structure

```
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   └── vehicle.py      # /vehicle-info route implementation
│   ├── core/
│   │   └── database.py         # SQLAlchemy engine and session setup
│   ├── models/
│   │   └── vehicle.py          # SQLAlchemy models
│   ├── schemas/
│   │   └── vehicle.py          # Pydantic validation schemas
│   └── main.py                 # FastAPI application initialization & router mounting
├── scripts/
│   ├── llm_instructions.md     # System prompt, constraints & car examples for Gemini
│   └── load_vehicles.py        # Python script to load LLM-generated data into DB
├── tests/
│   └── test_vehicle.py         # Unit and integration test suite
├── requirements.txt            # Python package dependencies
├── .env.example                # Template for environment configurations
└── .gitignore                  # Git ignore rules
```

---

## Setup & Installation

### 1. Prerequisite
Ensure you have Python 3.10+ installed on your system.

### 2. Set Up Virtual Environment
Create and activate a virtual environment to isolate project dependencies:

**On Windows (PowerShell)**:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**On Linux / macOS**:
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```
Open `.env` and fill in the following configurations:
- `DATABASE_URL`: Your Supabase connection string.
  > [!IMPORTANT]
  > Since Supabase direct database connection host is IPv6-only, ensure you use the **Connection Pooler URL** (using port **`6543`** in session mode) if your network is IPv4-only to avoid DNS lookup errors.
- `GEMINI_API_KEY`: Your Google Gemini API Key (required to run the AI database loader script).

---

## Running the Application

### Start the FastAPI Server
Run the application from the root directory as a module:
```bash
python -m app.main
```
Or directly with Uvicorn:
```bash
uvicorn app.main:app --reload
```
Once started, you can access the Swagger UI documentation locally at `http://127.0.0.1:8000/docs`.

### Run the Test Suite
The project includes unit and integration tests written in `pytest` which run in isolation using a temporary SQLite database:
```bash
pytest tests/
```

### Run the AI Database Loader Script
To request 100 realistic, unique vehicles from Gemini and load them into the database:
```bash
python scripts/load_vehicles.py
```
This script validates license plates to ensure they are **numbers only** with a length of **exactly 7 or 8 digits**, filters out duplicates, and commits new entries to your Supabase PostgreSQL database.

---

## API Documentation

### 1. `POST /vehicle-info`

Retrieves vehicle details based on the license plate.

- **Request Body**:
  ```json
  {
    "license_plate": "85647365"
  }
  ```

- **Successful Response (HTTP 200)**:
  ```json
  {
    "success": true,
    "data": {
      "license_plate": "85647365",
      "manufacturer": "Toyota",
      "model": "Corolla",
      "year": 2021,
      "color": "Silver"
    }
  }
  ```

- **Invalid Format Response (HTTP 400)**:
  Returned when the license plate is not numeric or length is not exactly 7 or 8 digits.
  ```json
  {
    "success": false,
    "error": "Invalid license plate format. Must be only numbers and 7 or 8 digits long."
  }
  ```

- **Vehicle Not Found (HTTP 404)**:
  Returned when the vehicle format is correct but does not exist in the database.
  ```json
  {
    "success": false,
    "error": "Vehicle not found"
  }
  ```

- **Validation Error (HTTP 422)**:
  Returned when query keys or formats do not match the required Pydantic schema structure.

---

### 2. `GET /health`

Lightweight server health status check.

- **Response (HTTP 200)**:
  ```json
  {
    "status": "healthy"
  }
  ```

---

Created with ❤️ by: Gal Helner