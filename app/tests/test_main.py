import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Helper function to obtain a valid token
def get_auth_headers():
    login_response = client.post("/auth/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200
    token = login_response.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}

def test_create_event():
    headers = get_auth_headers()  # Get authentication token
    response = client.post("/events/", json={
        "name": "Tech Conference",
        "description": "Annual tech meetup",
        "start_time": "2025-03-10T09:00:00",
        "end_time": "2025-03-10T18:00:00",
        "location": "New York",
        "max_attendees": 100
    }, headers=headers)  # Include token in the request
    
    assert response.status_code == 201
