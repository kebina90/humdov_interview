from fastapi.testclient import TestClient
from main import app
from database import engine, Base
import models


def setup_module():
    """This runs once before all tests in this module"""
    # Drop all tables and recreate them
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/users/",
        json={"username": "testuser"}
    )
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
    assert "id" in response.json()

def test_create_duplicate_user():
    client.post("/users/", json={"username": "duplicateuser"})
    
    response = client.post("/users/", json={"username": "duplicateuser"})
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

def test_get_feed_for_new_user():
    user_response = client.post("/users/", json={"username": "newuser"})
    user_id = user_response.json()["id"]

    client.post("/posts/", json={"title": "Test Post", "content": "Test Content", "tag": "test"})

    response = client.get(f"/users/{user_id}/feed")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_feed_for_nonexistent_user():
    response = client.get("/users/999/feed")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]