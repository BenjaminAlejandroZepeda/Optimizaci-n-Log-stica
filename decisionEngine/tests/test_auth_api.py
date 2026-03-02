

def test_register_success(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "user@test.com",
            "password": "123456",
        },
    )

    assert response.status_code == 201
    assert "id" in response.json()


def test_login_success(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@test.com",
            "password": "123456",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "login@test.com",
            "password": "123456",
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data


def test_me_success(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "me@test.com",
            "password": "123456",
        },
    )

    login = client.post(
        "/api/v1/auth/login",
        data={
            "username": "me@test.com",
            "password": "123456",
        },
    )

    token = login.json()["access_token"]

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == "me@test.com"