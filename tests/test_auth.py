def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={"email": "user1@example.com", "password": "securepass123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "user1@example.com"
    assert "id" in data


def test_register_duplicate_email(client):
    client.post(
        "/auth/register",
        json={"email": "dupe@example.com", "password": "securepass123"},
    )
    response = client.post(
        "/auth/register",
        json={"email": "dupe@example.com", "password": "anotherpass456"},
    )
    assert response.status_code == 400


def test_login_success(client):
    client.post(
        "/auth/register",
        json={"email": "login@example.com", "password": "securepass123"},
    )
    response = client.post(
        "/auth/login",
        data={"username": "login@example.com", "password": "securepass123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={"email": "wrongpass@example.com", "password": "securepass123"},
    )
    response = client.post(
        "/auth/login",
        data={"username": "wrongpass@example.com", "password": "incorrectpass"},
    )
    assert response.status_code == 401
