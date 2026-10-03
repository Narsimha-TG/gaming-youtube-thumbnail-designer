import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_analytics():
    response = client.get("/api/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "total_pickups" in data
    assert "completion_rate" in data

def test_create_pickup():
    payload = {
        "id": 2,
        "customer_name": "Jane Smith",
        "contact_phone": "555-0202",
        "pickup_address": "456 Oak Ave",
        "carpet_details": "Wool, 5x7",
        "status": "pending",
        "driver_id": None,
        "timestamp": "2023-10-28T12:00:00"
    }
    response = client.post("/api/pickups", json=payload)
    assert response.status_code == 200
    assert response.json()["customer_name"] == "Jane Smith"

def test_get_pickups_filtering():
    response = client.get("/api/pickups?status=pending")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_pickup_status():
    response = client.patch("/api/pickups/1/status?status=in-progress&driver_id=101")
    assert response.status_code == 200
    assert response.json()["status"] == "in-progress"
    assert response.json()["driver_id"] == 101