import pytest
from fastapi.testclient import TestClient
from app.main import app


class TestCalculatorAPI:
    """TDD unit tests for Calculator API endpoints"""

    def setup_method(self):
        """Set up test fixtures"""
        self.client = TestClient(app)

    def test_root_endpoint(self):
        """Test the root health check endpoint"""
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Calculator API is running"}

    def test_add_endpoint_success(self):
        """Test successful addition via API"""
        response = self.client.post("/add", json={"num1": 2, "num2": 3})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 5
        assert data["operation"] == "addition"

    def test_add_endpoint_with_floats(self):
        """Test addition with floating point numbers"""
        response = self.client.post("/add", json={"num1": 2.5, "num2": 3.7})
        assert response.status_code == 200
        assert response.json()["result"] == pytest.approx(6.2)

    def test_subtract_endpoint_success(self):
        """Test successful subtraction via API"""
        response = self.client.post("/subtract", json={"num1": 10, "num2": 4})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 6
        assert data["operation"] == "subtraction"

    def test_multiply_endpoint_success(self):
        """Test successful multiplication via API"""
        response = self.client.post("/multiply", json={"num1": 3, "num2": 4})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 12
        assert data["operation"] == "multiplication"

    def test_divide_endpoint_success(self):
        """Test successful division via API"""
        response = self.client.post("/divide", json={"num1": 10, "num2": 2})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 5
        assert data["operation"] == "division"

    def test_divide_by_zero_returns_error(self):
        """Test that dividing by zero returns 400 error"""
        response = self.client.post("/divide", json={"num1": 10, "num2": 0})
        assert response.status_code == 400
        assert "Cannot divide by zero" in response.json()["detail"]

    def test_invalid_request_missing_fields(self):
        """Test that missing required fields returns 422 error"""
        response = self.client.post("/add", json={"num1": 5})
        assert response.status_code == 422

    def test_invalid_request_wrong_types(self):
        """Test that wrong data types return 422 error"""
        response = self.client.post("/add", json={"num1": "invalid", "num2": 3})
        assert response.status_code == 422
