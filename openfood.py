import requests

BASE_URL = "https://world.openfoodfacts.org/api/v0/product"


def get_product_by_barcode(barcode):
    """
    Fetch product details from OpenFoodFacts using a barcode.
    """

    url = f"{BASE_URL}/{barcode}.json"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get("status") == 1:
            product = data.get("product", {})

            return {
                "name": product.get("product_name", "Unknown Product"),
                "brand": product.get("brands", "Unknown Brand"),
                "ingredients": product.get("ingredients_text", "Not Available"),
                "barcode": barcode
            }

        return None

    except requests.RequestException:
        return None