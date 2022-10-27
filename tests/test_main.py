import pytest
import json
import time
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)


def test_main():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "Still Alive"}


def test_get_empty_data():
    response = client.get("/search?query=")
    assert response.status_code == 200
    assert response.json() == "No Results Found"


def test_get_data():
    response = client.get("/search?query=baba")
    assert response.status_code == 200
    assert response.json() != []
