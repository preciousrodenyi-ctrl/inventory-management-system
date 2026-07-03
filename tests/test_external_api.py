from unittest.mock import Mock, patch

from openfood import fetch_product_details


def test_fetch_product_details_by_barcode():
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Water, almonds",
            "code": "1234567890123"
        }
    }

    with patch("openfood.requests.get", return_value=mock_response):
        product = fetch_product_details("1234567890123")

    assert product["product_name"] == "Organic Almond Milk"
    assert product["brands"] == "Silk"
    assert product["barcode"] == "1234567890123"
    assert product["source"] == "OpenFoodFacts"


def test_fetch_product_details_by_name():
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "products": [
            {
                "product_name": "Oat Milk",
                "brands": "Oatly",
                "ingredients_text": "Water, oats",
                "code": "1111111111111"
            }
        ]
    }

    with patch("openfood.requests.get", return_value=mock_response):
        product = fetch_product_details("Oat Milk")

    assert product["product_name"] == "Oat Milk"
    assert product["brands"] == "Oatly"