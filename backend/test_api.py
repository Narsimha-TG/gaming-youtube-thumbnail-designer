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
    assert "total_items" in data
    assert "average_score" in data

def test_submit_review():
    payload = {
        "id": 3,
        "title": "New Thumbnail Design",
        "status": "active",
        "score": 9.0,
        "timestamp": "2023-10-27T12:00:00Z"
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Review submitted successfully"

def test_update_theme():
    payload = {"theme_preference": "light"}
    response = client.patch("/api/settings/theme", json=payload)
    assert response.status_code == 200
    assert response.json()["theme_preference"] == "light"

def test_update_theme_invalid():
    payload = {"theme_preference": "neon"}
    response = client.patch("/api/settings/theme", json=payload)
    assert response.status_code == 400