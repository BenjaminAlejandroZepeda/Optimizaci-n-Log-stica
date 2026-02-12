from fastapi.testclient import TestClient
from decisionengine.main import create_app
from datetime import timedelta

app = create_app()
client = TestClient(app)


def build_order_payload():
    return {
        "origin": {"lat": 0, "lon": 0},
        "destination": {"lat": 1, "lon": 1},
        "weight_kg": 10,
        "priority": "HIGH",
        "required_vehicle_type": "BIKE",
        "max_wait_time_min": 30,
    }


def test_assign_success():
    response = client.post(
        "/api/v1/decisions/assign",
        json=build_order_payload(),
    )

    assert response.status_code == 200

    data = response.json()

    # Debe devolver al menos vehicle, route y score
    assert "vehicle" in data
    assert "route" in data
    assert "score" in data
    assert isinstance(data["score"], float)


def test_assign_with_debug():
    response = client.post(
        "/api/v1/decisions/assign?debug=true",
        json=build_order_payload(),
    )

    assert response.status_code == 200

    data = response.json()

    # Cuando debug=true debe incluir debug
    assert "debug" in data
    assert data["debug"] is not None


def test_assign_invalid_vehicle_type():
    payload = build_order_payload()
    payload["required_vehicle_type"] = "PLANE"

    response = client.post(
        "/api/v1/decisions/assign",
        json=payload,
    )

    # Puede ser 400 (mapper) o 422 (pydantic)
    assert response.status_code in (400, 422)


def test_preview_success():
    response = client.post(
        "/api/v1/decisions/preview",
        json=build_order_payload(),
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    # Si hay resultados, deben tener score
    if data:
        assert "score" in data[0]
