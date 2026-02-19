def test_register(client):
    response = client.post(
        "auth/register",
        json={"email": "test@example.com", "password": "secret"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "test@example.com"
    assert "id" in data


def test_register_and_token(client):
    r = client.post("auth/register", json={"email": "a@test.com", "password": "secret"})
    assert r.status_code == 200, r.text

    t = client.post("auth/token", data={"username": "a@test.com", "password": "secret"})
    assert r.status_code == 200, t.text

    token_data = t.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
