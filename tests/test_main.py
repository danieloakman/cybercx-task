import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestSubmitRoute:
    """Test cases for the /submit route"""

    def test_submit_valid_payload(self):
        """Test submitting a valid payload"""

        response = client.post(
            "/submit", json={"value": "example.org", "tags": ["something"]}
        )

        assert response.status_code == 201
        assert response.json() == -6547282170865453948

    def test_submit_invalid_payload(self):
        """Test submitting an invalid payload"""

        response = client.post(
            "/submit", json={"value": "test value", "tags": ["tag1", "tag2", "tag3"]}
        )

        assert response.status_code == 400
        assert response.json() == {"message": "Invalid value format"}


class TestHealthRoute:
    """Test cases for the /health route"""

    def test_health_check(self):
        """Test the health check endpoint"""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


if __name__ == "__main__":
    pytest.main([__file__])
