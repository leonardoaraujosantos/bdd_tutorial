import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Fixture to provide a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def context():
    """Fixture to provide a shared context for BDD scenarios"""
    return {}
