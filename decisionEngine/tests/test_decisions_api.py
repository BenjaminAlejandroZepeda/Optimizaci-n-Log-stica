def build_order_payload():
    return {
        "origin": {"lat": 0, "lon": 0},
        "destination": {"lat": 0, "lon": 1},
        "weight_kg": 10,
        "priority": "HIGH",
        "required_vehicle_type": "BIKE",
        "max_wait_time_min": 30,
    }


def get_auth_headers(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@test.com",
            "password": "123456",
        },
    )

    login = client.post(
        "/api/v1/auth/login",
        data={
            "username": "test@test.com",
            "password": "123456",
        },
    )

    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_assign_success(client):
    headers = get_auth_headers(client)

    response = client.post(
        "/api/v1/decisions/assign",
        json=build_order_payload(),
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()

    assert "vehicle" in data
    assert "route" in data
    assert "score" in data


def test_preview_success(client):
    headers = get_auth_headers(client)

    response = client.post(
        "/api/v1/decisions/preview",
        json=build_order_payload(),
        headers=headers,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)