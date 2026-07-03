def register_and_login(client, email="cattest@example.com", password="securepass123"):
    client.post("/auth/register", json={"email": email, "password": password})
    response = client.post(
        "/auth/login", data={"username": email, "password": password}
    )
    return response.json()["access_token"]


def test_create_category(client):
    token = register_and_login(client)
    response = client.post(
        "/categories/",
        json={"name": "Electronics", "description": "Gadgets"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Electronics"
    assert "id" in data


def test_create_category_requires_auth(client):
    response = client.post(
        "/categories/", json={"name": "Books", "description": "Reading material"}
    )
    assert response.status_code == 401


def test_list_categories(client):
    token = register_and_login(client)
    client.post(
        "/categories/",
        json={"name": "Toys", "description": "Fun stuff"},
        headers={"Authorization": f"Bearer {token}"},
    )
    response = client.get("/categories/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_category_not_found(client):
    response = client.get("/categories/999")
    assert response.status_code == 404


def test_delete_category(client):
    token = register_and_login(client)
    create_response = client.post(
        "/categories/",
        json={"name": "Temporary", "description": "Will be deleted"},
        headers={"Authorization": f"Bearer {token}"},
    )
    category_id = create_response.json()["id"]
    delete_response = client.delete(
        f"/categories/{category_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert delete_response.status_code == 204
    get_response = client.get(f"/categories/{category_id}")
    assert get_response.status_code == 404
