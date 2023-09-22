from geocoder_api.__main__ import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_healthcheck():
    response = client.get("/health")
    assert response.status_code == 200
