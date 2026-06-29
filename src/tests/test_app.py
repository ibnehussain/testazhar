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


def test_get_activities_returns_all():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


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


def test_activity_is_full_returns_spots_remaining_when_not_full():
    response = client.get("/activities/Programming Class/is-full")
    assert response.status_code == 200
    assert response.json() == {
        "activity": "Programming Class",
        "is_full": False,
        "spots_remaining": 18,
    }


def test_activity_is_full_returns_true_when_full():
    activities["Chess Club"]["participants"] = [
        f"student{i}@mergington.edu" for i in range(12)
    ]

    response = client.get("/activities/Chess Club/is-full")
    assert response.status_code == 200
    assert response.json() == {
        "activity": "Chess Club",
        "is_full": True,
    }


def test_activity_is_full_invalid_activity():
    response = client.get("/activities/Nonexistent Activity/is-full")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


# ============================================================
# Tests for /api/ask endpoint (Capstone)
# ============================================================

def test_ask_qualitative_question():
    """Test /api/ask with a qualitative question routes to RAG."""
    response = client.post(
        "/api/ask",
        json={"question": "Tell me about Chess Club"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "source" in data
    assert "confidence" in data
    assert data["source"] == "rag"


def test_ask_quantitative_question():
    """Test /api/ask with a quantitative question routes to Text2SQL."""
    response = client.post(
        "/api/ask",
        json={"question": "How many students are in Programming Class?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "source" in data
    assert "confidence" in data
    assert data["source"] == "text2sql"


def test_ask_unknown_question():
    """Test /api/ask with an unknown question type routes to direct."""
    response = client.post(
        "/api/ask",
        json={"question": "xyzabc random nonsense question"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "source" in data
    assert "confidence" in data
    assert data["source"] == "direct"


def test_ask_missing_question_field():
    """Test /api/ask without question field returns 400."""
    response = client.post(
        "/api/ask",
        json={}
    )
    assert response.status_code == 400
    data = response.json()
    assert "error" in data


def test_ask_empty_question_string():
    """Test /api/ask with empty question string returns 400."""
    response = client.post(
        "/api/ask",
        json={"question": ""}
    )
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
