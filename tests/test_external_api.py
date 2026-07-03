from unittest.mock import patch

from openfood import (
    search_by_barcode,
    search_by_name
)


@patch("openfood.requests.get")
def test_search_barcode(mock_get):

    mock_get.return_value.status_code = 200

    mock_get.return_value.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Milk",
            "brands": "Brookside",
            "ingredients_text": "Milk"
        }
    }

    product = search_by_barcode("12345")

    assert product["product_name"] == "Milk"


@patch("openfood.requests.get")
def test_search_name(mock_get):

    mock_get.return_value.status_code = 200

    mock_get.return_value.json.return_value = {
        "products": [
            {
                "product_name": "Juice",
                "brands": "Minute Maid",
                "code": "11111"
            }
        ]
    }

    products = search_by_name("juice")

    assert len(products) == 1