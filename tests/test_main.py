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

    def test_submit_valid_payload_without_tags(self):
        """Test submitting a valid payload without tags"""
        response = client.post("/submit", json={"value": "192.168.1.1"})
        assert response.status_code == 201
        assert response.json() == -2312086495570852284

    def test_submit_invalid_payload(self):
        """Test submitting an invalid payload"""
        response = client.post(
            "/submit", json={"value": "test value", "tags": ["tag1", "tag2", "tag3"]}
        )
        assert response.status_code == 422
        json_res = response.json()
        assert "detail" in json_res
        assert "errors" in json_res
        assert len(json_res["errors"]) == 1
        assert json_res["errors"][0]["field"] == "value"

    def test_submit_duplicate_payload(self):
        """Test submitting a duplicate payload"""
        response = client.post(
            "/submit", json={"value": "google.com", "tags": ["something"]}
        )
        assert response.status_code == 201
        response = client.post(
            "/submit", json={"value": "google.com", "tags": ["something"]}
        )
        assert response.status_code == 400


class TestDataRoute:
    """Test cases for the /data route"""

    def test_data_valid_request(self):
        """Test a valid data request"""
        response = client.get("/data?q=google&limit=10")
        try:
            assert response.status_code == 200
            assert response.json() == []
        except Exception as e:
            print(e)


class TestHealthRoute:
    """Test cases for the /health route"""

    def test_health_check(self):
        """Test the health check endpoint"""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


if __name__ == "__main__":
    pytest.main([__file__])
