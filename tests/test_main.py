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

    def test_submit_md5_payload(self):
        """Test submitting a MD5 payload"""
        response = client.post(
            "/submit",
            json={"value": "d41d8cd98f00b204e9800998ecf8427e", "tags": ["something"]},
        )
        assert response.status_code == 201

    def test_submit_sha1_payload(self):
        """Test submitting a SHA1 payload"""
        response = client.post(
            "/submit",
            json={
                "value": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
                "tags": ["something"],
            },
        )
        assert response.status_code == 201

    def test_submit_sha256_payload(self):
        """Test submitting a SHA256 payload"""
        response = client.post(
            "/submit",
            json={
                "value": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            },
        )
        assert response.status_code == 201


class TestDataRoute:
    """Test cases for the /data route"""

    def test_data_valid_request(self):
        """Test a valid data request"""
        response = client.get("/data?q=google.com&limit=1")
        assert response.status_code == 200
        results = response.json()
        assert len(results) == 1
        assert results[0]["value"] == "google.com"
        assert results[0]["tags"] == ["something"]
        assert results[0]["type"] == "domain"

    def test_data_valid_request_with_tags(self):
        """Test a valid data request with tags"""
        for i in range(10):
            response = client.post(
                "/submit", json={"value": "google.com", "tags": ["a", str(i)]}
            )
            assert response.status_code == 201
        response = client.get("/data?q=google.com&limit=20&tags=A")
        assert response.status_code == 200
        results = response.json()
        assert len(results) == 10
        assert results[0]["value"] == "google.com"
        assert results[0]["tags"] == ["a", "0"]

    def test_data_request_has_valid_types(self):
        """Test that the data request has valid types"""
        response = client.post("/submit", json={"value": "1.1.1.1"})
        assert response.status_code == 201
        response = client.get("/data?q=1.1.1.1&limit=1")
        assert response.status_code == 200
        results = response.json()
        assert results[0]["type"] == "ip"

        response = client.post("/submit", json={"value": "google.com"})
        assert response.status_code == 201
        response = client.get("/data?q=google.com&limit=1")
        assert response.status_code == 200
        results = response.json()
        assert results[0]["type"] == "domain"

        response = client.post(
            "/submit", json={"value": "d41d8cd98f00b204e9800998ecf8427e"}
        )
        assert response.status_code == 201
        response = client.get("/data?q=d41d8cd98f00b204e9800998ecf8427e&limit=1")
        assert response.status_code == 200
        results = response.json()
        assert results[0]["type"] == "hash"


class TestHealthRoute:
    """Test cases for the /health route"""

    def test_health_check(self):
        """Test the health check endpoint"""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


if __name__ == "__main__":
    pytest.main([__file__])
