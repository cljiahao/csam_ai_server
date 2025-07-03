from fastapi.testclient import TestClient


def test_home(test_client: TestClient) -> None:
    """Test the root endpoint of the FastAPI application."""

    response = test_client.get("/")

    assert response.status_code == 200
    assert response.json() == {"msg": "Hello Fast_API 🚀"}


def test_health(test_client: TestClient) -> None:
    """Test the /health endpoint of the FastAPI application."""

    response = test_client.get("/v2/health")

    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
