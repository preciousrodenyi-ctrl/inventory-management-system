import pytest
from unittest.mock import patch

from app import app
from inventory import reset_store


@pytest.fixture(autouse=True)
def setup_and_teardown():
    reset_store()
    yield
    reset_store()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_inventory(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_get_single_item(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["id"] == 1


def test_create_item(client):
    response = client.post("/inventory", json={
        "product_name": "Cashew Milk",
        "brands": "Simple Truth",
        "ingredients_text": "Water, cashews",
        "barcode": "9999999999999",
        "price": 4.25,
        "stock": 12
    })
    assert response.status_code == 201
    assert response.get_json()["product_name"] == "Cashew Milk"


def test_patch_item(client):
    response = client.patch("/inventory/1", json={"price": 5.55, "stock": 99})
    assert response.status_code == 200
    data = response.get_json()
    assert data["price"] == 5.55
    assert data["stock"] == 99


def test_delete_item(client):
    response = client.delete("/inventory/1")
    assert response.status_code == 200
    follow_up = client.get("/inventory/1")
    assert follow_up.status_code == 404


def test_import_item(client):
    fake_product = {
        "product_name": "Imported Protein Bar",
        "brands": "Test Brand",
        "ingredients_text": "Protein, oats",
        "barcode": "7777777777777",
        "price": 0.0,
        "stock": 0,
        "source": "OpenFoodFacts"
    }

    with patch("app.fetch_product_details", return_value=fake_product):
        response = client.post("/inventory/import", json={"barcode": "7777777777777"})

    assert response.status_code == 201
    assert response.get_json()["product_name"] == "Imported Protein Bar"


def test_search_openfoodfacts(client):
    fake_product = {
        "product_name": "Search Result Milk",
        "brands": "Search Brand",
        "ingredients_text": "Milk",
        "barcode": "8888888888888",
        "price": 0.0,
        "stock": 0,
        "source": "OpenFoodFacts"
    }

    with patch("app.fetch_product_details", return_value=fake_product):
        response = client.get("/openfoodfacts/search?query=milk")

    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Search Result Milk"