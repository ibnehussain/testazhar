"""
Tests for the Mergington High School API
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset participant lists before each test to avoid state leakage."""
    original = {name: {**data, "participants": list(data["participants"])}
                for name, data in activities.items()}
    yield
    for name, data in original.items():
        activities[name]["participants"] = data["participants"]


client = TestClient(app)


 


def test_get_activities_has_expected_fields():
    response = client.get("/activities")
    data = response.json()
    for activity in data.values():
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity


def test_signup_success():
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    assert response.status_code == 200
    assert "newstudent@mergington.edu" in response.json()["message"]


def test_signup_invalid_activity():
    response = client.post(
        "/activities/Nonexistent Activity/signup",
        params={"email": "student@mergington.edu"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_root_redirects():
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (302, 307)
    assert "/static/index.html" in response.headers["location"]


def test_get_activity_valid_name():
    response = client.get("/activities/Chess Club")
    assert response.status_code == 200
    assert response.json() == activities["Chess Club"]


def test_get_activity_unknown_name():
    response = client.get("/activities/Unknown Activity")
    assert response.status_code == 404
    assert response.json() == {"error": "Activity not found"}


def test_get_activity_empty_name():
    response = client.get("/activities/")
    assert response.status_code == 404
    assert response.json() == {"error": "Activity not found"}
