import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

INITIAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball training and games",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn tennis techniques and participate in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["sarah@mergington.edu"]
    },
    "Art Studio": {
        "description": "Painting, drawing, and sculpture techniques",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["maya@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting, theater production, and performance",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["alex@mergington.edu", "jordan@mergington.edu"]
    },
    "Debate Society": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["chris@mergington.edu"]
    },
    "Science Club": {
        "description": "Explore physics, chemistry, and biology through experiments",
        "schedule": "Tuesdays, 3:30 PM - 4:45 PM",
        "max_participants": 15,
        "participants": ["rachel@mergington.edu", "noah@mergington.edu"]
    }
}

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: Reset activities to initial state before each test
    activities.clear()
    activities.update(INITIAL_ACTIVITIES)

def test_get_activities():
    # Arrange: None needed (fixture handles setup)
    
    # Act: Make GET request to /activities
    response = client.get("/activities")
    
    # Assert: Check status and data
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]

def test_signup_success():
    # Arrange: None needed
    
    # Act: Make POST request to signup
    response = client.post("/activities/Chess Club/signup?email=new@student.edu")
    
    # Assert: Check status, message, and participant added
    assert response.status_code == 200
    assert response.json() == {"message": "Signed up new@student.edu for Chess Club"}
    assert "new@student.edu" in activities["Chess Club"]["participants"]

def test_signup_activity_not_found():
    # Arrange: None needed
    
    # Act: Make POST request with invalid activity
    response = client.post("/activities/Nonexistent/signup?email=test@email.com")
    
    # Assert: Check 404 and error message
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}

def test_signup_already_signed_up():
    # Arrange: None needed
    
    # Act: Make POST request for already signed-up email
    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")
    
    # Assert: Check 400 and error message
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up"}

def test_unregister_success():
    # Arrange: None needed
    
    # Act: Make DELETE request to unregister
    response = client.delete("/activities/Chess Club/signup?email=michael@mergington.edu")
    
    # Assert: Check status, message, and participant removed
    assert response.status_code == 200
    assert response.json() == {"message": "Unregistered michael@mergington.edu from Chess Club"}
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]

def test_unregister_activity_not_found():
    # Arrange: None needed
    
    # Act: Make DELETE request with invalid activity
    response = client.delete("/activities/Nonexistent/signup?email=test@email.com")
    
    # Assert: Check 404 and error message
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}

def test_unregister_participant_not_found():
    # Arrange: None needed
    
    # Act: Make DELETE request for non-participant
    response = client.delete("/activities/Chess Club/signup?email=not@signed.up")
    
    # Assert: Check 404 and error message
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found"}