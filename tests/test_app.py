import json


def test_home_page(client):
    """Test the home page loads successfully."""
    response = client.get("/")
    assert response.status_code == 200


def test_get_all_inventory(client):
    """Test retrieving all inventory items."""
    response = client.get("/inventory")

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_single_item(client):
    """Test retrieving an existing inventory item."""
    response = client.get("/inventory/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == 1
    assert "product_name" in data


def test_get_nonexistent_item(client):
    """Test requesting an item that does not exist."""
    response = client.get("/inventory/999")

    assert response.status_code == 404

    assert response.get_json()["error"] == "Item not found"


def test_create_item(client):
    """Test creating a new inventory item."""

    new_product = {
        "product_name": "Rice",
        "brand": "Daawat",
        "price": 350,
        "stock": 20,
        "barcode": "1234567890"
    }

    response = client.post(
        "/inventory",
        data=json.dumps(new_product),
        content_type="application/json"
    )

    assert response.status_code == 201

    product = response.get_json()

    assert product["product_name"] == "Rice"
    assert product["brand"] == "Daawat"
    assert product["price"] == 350
    assert product["stock"] == 20


def test_create_item_missing_fields(client):
    """Test creating a product with missing required fields."""

    incomplete_product = {
        "product_name": "Sugar"
    }

    response = client.post(
        "/inventory",
        data=json.dumps(incomplete_product),
        content_type="application/json"
    )

    assert response.status_code == 400


def test_update_item(client):
    """Test updating an existing product."""

    update_data = {
        "price": 500,
        "stock": 40
    }

    response = client.patch(
        "/inventory/1",
        data=json.dumps(update_data),
        content_type="application/json"
    )

    assert response.status_code == 200

    updated = response.get_json()

    assert updated["price"] == 500
    assert updated["stock"] == 40


def test_update_nonexistent_item(client):
    """Test updating an item that doesn't exist."""

    response = client.patch(
        "/inventory/999",
        data=json.dumps({"price": 100}),
        content_type="application/json"
    )

    assert response.status_code == 404


def test_delete_item(client):
    """Test deleting an existing item."""

    response = client.delete("/inventory/2")

    assert response.status_code == 200

    assert response.get_json()["message"] == "Item deleted successfully"


def test_delete_nonexistent_item(client):
    """Test deleting a product that doesn't exist."""

    response = client.delete("/inventory/999")

    assert response.status_code == 404