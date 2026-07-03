def register_and_login(client, email="prodtest@example.com", password="securepass123"):
    client.post("/auth/register", json={"email": email, "password": password})
    response = client.post(
        "/auth/login", data={"username": email, "password": password}
    )
    return response.json()["access_token"]


def create_category(client, token, name="Electronics"):
    response = client.post(
        "/categories/",
        json={"name": name, "description": "Test category"},
        headers={"Authorization": f"Bearer {token}"},
    )
    return response.json()["id"]


def test_create_product(client):
    token = register_and_login(client)
    category_id = create_category(client, token)
    response = client.post(
        "/products/",
        json={
            "name": "Laptop",
            "description": "15-inch",
            "price": 999.99,
            "stock_quantity": 10,
            "category_id": category_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["category_id"] == category_id


def test_create_product_invalid_category(client):
    token = register_and_login(client)
    response = client.post(
        "/products/",
        json={
            "name": "Ghost",
            "description": "test",
            "price": 1,
            "stock_quantity": 1,
            "category_id": 999,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400


def test_update_product(client):
    token = register_and_login(client)
    category_id = create_category(client, token)
    create_response = client.post(
        "/products/",
        json={
            "name": "Phone",
            "description": "Smartphone",
            "price": 599.99,
            "stock_quantity": 5,
            "category_id": category_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    product_id = create_response.json()["id"]
    update_response = client.put(
        f"/products/{product_id}",
        json={"price": 549.99, "stock_quantity": 3},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["price"] == 549.99
    assert data["stock_quantity"] == 3
    assert data["name"] == "Phone"


def test_delete_product(client):
    token = register_and_login(client)
    category_id = create_category(client, token)
    create_response = client.post(
        "/products/",
        json={
            "name": "Tablet",
            "description": "10-inch",
            "price": 299.99,
            "stock_quantity": 7,
            "category_id": category_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    product_id = create_response.json()["id"]
    delete_response = client.delete(
        f"/products/{product_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert delete_response.status_code == 204
    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404


def test_filter_products_by_category(client):
    token = register_and_login(client)
    electronics_id = create_category(client, token, name="Electronics")
    books_id = create_category(client, token, name="Books")
    client.post(
        "/products/",
        json={
            "name": "Monitor",
            "description": "4K",
            "price": 399.99,
            "stock_quantity": 2,
            "category_id": electronics_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    client.post(
        "/products/",
        json={
            "name": "Novel",
            "description": "Fiction",
            "price": 14.99,
            "stock_quantity": 20,
            "category_id": books_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    response = client.get(f"/products/?category_id={electronics_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "Monitor"
