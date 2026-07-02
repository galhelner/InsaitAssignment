import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.main import app
from app.api.endpoints.vehicle import get_db
import app.models as models

# Use a file-based SQLite database for testing to maintain schema state across connections
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_temp.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency for tests
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    # Setup: Create tables and insert mock data before each test
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Add a mock vehicle
    db_vehicle = models.Vehicle(
        license_plate="12345678",
        manufacturer="Toyota",
        model="Corolla",
        year=2021,
        color="Silver"
    )
    db.add(db_vehicle)
    db.commit()
    db.close()
    
    yield
    
    # Teardown: Drop tables after each test to ensure isolation
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test_temp.db"):
        try:
            os.remove("./test_temp.db")
        except Exception:
            pass

def test_get_vehicle_info_success():
    response = client.post(
        "/vehicle-info",
        json={"license_plate": "12345678"}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert json_data["data"]["license_plate"] == "12345678"
    assert json_data["data"]["manufacturer"] == "Toyota"
    assert json_data["data"]["model"] == "Corolla"
    assert json_data["data"]["year"] == 2021
    assert json_data["data"]["color"] == "Silver"
    assert json_data["error"] is None

def test_get_vehicle_info_not_found():
    response = client.post(
        "/vehicle-info",
        json={"license_plate": "99999999"}
    )
    assert response.status_code == 404
    json_data = response.json()
    assert json_data["success"] is False
    assert "data" not in json_data
    assert json_data["error"] == "Vehicle not found"

def test_get_vehicle_info_invalid_format():
    # Case 1: Contains letters
    response = client.post(
        "/vehicle-info",
        json={"license_plate": "1234567a"}
    )
    assert response.status_code == 400
    json_data = response.json()
    assert json_data["success"] is False
    assert "data" not in json_data
    assert "Invalid license plate format" in json_data["error"]

    # Case 2: Too short (6 digits)
    response = client.post(
        "/vehicle-info",
        json={"license_plate": "123456"}
    )
    assert response.status_code == 400

    # Case 3: Too long (9 digits)
    response = client.post(
        "/vehicle-info",
        json={"license_plate": "123456789"}
    )
    assert response.status_code == 400

    # Case 4: Valid length 7 but doesn't exist -> should return 404 (not 400)
    response = client.post(
        "/vehicle-info",
        json={"license_plate": "1234567"}
    )
    assert response.status_code == 404

def test_get_vehicle_info_invalid_request():
    # Request body missing 'license_plate'
    response = client.post(
        "/vehicle-info",
        json={}
    )
    # FastAPI returns 422 Unprocessable Entity for invalid request bodies
    assert response.status_code == 422
