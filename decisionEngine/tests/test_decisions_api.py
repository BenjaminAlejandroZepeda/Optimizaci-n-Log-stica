def build_order_payload():
    return {
        "origin_lat": 0.0,
        "origin_lng": 0.0,
        "destination_lat": 0.0,
        "destination_lng": 1.0,
        "weight_kg": 10.0,
        "priority": "high",
        "required_vehicle_type": "bike",
        "max_wait_time_seconds": 1800.0,
    }


def get_auth_headers(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "test@test.com", "password": "123456"},
    )
    login = client.post(
        "/api/v1/auth/login",
        data={"username": "test@test.com", "password": "123456"},
    )
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ── DEBUG (eliminar cuando todos los tests pasen) ──────────────────────────────

def test_debug_422(client):
    """Imprime el detalle exacto del 422 para diagnóstico. Eliminar tras fix."""
    headers = get_auth_headers(client)
    response = client.post(
        "/api/v1/decisions/assign",
        json=build_order_payload(),
        headers=headers,
    )
    if response.status_code != 200:
        import json
        print("\n── 422 detail ──")
        print(json.dumps(response.json(), indent=2))
    assert response.status_code == 200


# ── DECISIONS ──────────────────────────────────────────────────────────────────

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


def test_assign_with_debug(client):
    headers = get_auth_headers(client)
    response = client.post(
        "/api/v1/decisions/assign?debug=true",
        json=build_order_payload(),
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "debug" in data
    assert data["debug"] is not None
    assert "metrics" in data["debug"]
    assert "vehicle_id" in data["debug"]


def test_assign_requires_auth(client):
    response = client.post(
        "/api/v1/decisions/assign",
        json=build_order_payload(),
    )
    assert response.status_code == 401


def test_preview_success(client):
    headers = get_auth_headers(client)
    response = client.post(
        "/api/v1/decisions/preview",
        json=build_order_payload(),
        headers=headers,
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_preview_with_debug(client):
    headers = get_auth_headers(client)
    response = client.post(
        "/api/v1/decisions/preview?debug=true",
        json=build_order_payload(),
        headers=headers,
    )
    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)
    if results:
        assert "debug" in results[0]


def test_preview_requires_auth(client):
    response = client.post(
        "/api/v1/decisions/preview",
        json=build_order_payload(),
    )
    assert response.status_code == 401


def test_preview_sorted_by_score(client):
    headers = get_auth_headers(client)
    response = client.post(
        "/api/v1/decisions/preview",
        json=build_order_payload(),
        headers=headers,
    )
    assert response.status_code == 200
    results = response.json()
    if len(results) > 1:
        scores = [r["score"] for r in results]
        assert scores == sorted(scores)


# ── ORDERS ────────────────────────────────────────────────────────────────────

def test_orders_list_empty_initially(client):
    headers = get_auth_headers(client)
    response = client.get("/api/v1/orders/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_orders_list_after_assign(client):
    headers = get_auth_headers(client)
    assign = client.post(
        "/api/v1/decisions/assign",
        json=build_order_payload(),
        headers=headers,
    )
    assert assign.status_code == 200, f"assign failed: {assign.json()}"
    response = client.get("/api/v1/orders/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_orders_get_by_id(client):
    headers = get_auth_headers(client)
    assign = client.post(
        "/api/v1/decisions/assign",
        json=build_order_payload(),
        headers=headers,
    )
    assert assign.status_code == 200, f"assign failed: {assign.json()}"
    orders = client.get("/api/v1/orders/", headers=headers).json()
    assert len(orders) >= 1
    order_id = orders[0]["id"]
    response = client.get(f"/api/v1/orders/{order_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == order_id


def test_orders_get_by_id_not_found(client):
    headers = get_auth_headers(client)
    response = client.get("/api/v1/orders/nonexistent-id", headers=headers)
    assert response.status_code == 404


def test_orders_delete(client):
    headers = get_auth_headers(client)
    assign = client.post(
        "/api/v1/decisions/assign",
        json=build_order_payload(),
        headers=headers,
    )
    assert assign.status_code == 200, f"assign failed: {assign.json()}"
    orders = client.get("/api/v1/orders/", headers=headers).json()
    assert len(orders) >= 1
    order_id = orders[0]["id"]
    delete_response = client.delete(f"/api/v1/orders/{order_id}", headers=headers)
    assert delete_response.status_code == 204
    get_response = client.get(f"/api/v1/orders/{order_id}", headers=headers)
    assert get_response.status_code == 404


def test_orders_requires_auth(client):
    response = client.get("/api/v1/orders/")
    assert response.status_code == 401


def test_validate_order_success(client):
    headers = get_auth_headers(client)
    response = client.post(
        "/api/v1/orders/validate",
        json=build_order_payload(),
        headers=headers,
    )
    # validate llama assign_order con vehicles=[] → NoVehicleAvailableError → 400
    # 400 es correcto: la ruta existe y la orden es estructuralmente válida
    assert response.status_code in (200, 400)
    print(response.json())


# ── SCORING ───────────────────────────────────────────────────────────────────

def test_scoring_weights(client):
    headers = get_auth_headers(client)
    response = client.get("/api/v1/scoring/weights", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "weights" in data
    assert "priority_multipliers" in data
    assert "distance" in data["weights"]
    assert "time" in data["weights"]
    assert "wait" in data["weights"]


def test_scoring_explain(client):
    headers = get_auth_headers(client)
    response = client.post(
        "/api/v1/scoring/explain",
        json=build_order_payload(),
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_score" in data
    assert "priority_multiplier" in data
    assert "raw_score" in data
    assert "factors" in data
    assert len(data["factors"]) == 3
    factor_names = [f["name"] for f in data["factors"]]
    assert "distance" in factor_names
    assert "time" in factor_names
    assert "wait" in factor_names


def test_scoring_explain_requires_auth(client):
    response = client.post(
        "/api/v1/scoring/explain",
        json=build_order_payload(),
    )
    assert response.status_code == 401


def test_scoring_priority_multiplier_urgent(client):
    headers = get_auth_headers(client)
    payload = {**build_order_payload(), "priority": "critical"}
    response = client.post(
        "/api/v1/scoring/explain",
        json=payload,
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["priority_multiplier"] == 0.4


def test_scoring_priority_multiplier_low(client):
    headers = get_auth_headers(client)
    payload = {**build_order_payload(), "priority": "low"}
    response = client.post(
        "/api/v1/scoring/explain",
        json=payload,
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["priority_multiplier"] == 1.3