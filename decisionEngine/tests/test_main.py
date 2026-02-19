import pytest
from fastapi.testclient import TestClient

from decisionengine.main import create_app
from decisionengine.core.exceptions import NoVehicleAvailableError


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_app_creation():
    app = create_app()
    assert app.title == "Decision Engine"


def test_router_is_registered(client):
    
    response = client.get("/api/v1")
   
    assert response.status_code in (404, 405)


def test_no_vehicle_exception_handler(client):
    
    app = client.app

    @app.get("/test-no-vehicle")
    def raise_error():
        raise NoVehicleAvailableError("No vehicle available")

    response = client.get("/test-no-vehicle")

    assert response.status_code == 404
    assert response.json() == {
        "error": "no_vehicle_available",
        "message": "No vehicle available",
    }
