import requests


def normalize_product(product):
    return {
        "product_name": product.get("product_name") or product.get("product_name_en") or "Unknown Product",
        "brands": product.get("brands") or "Unknown Brand",
        "ingredients_text": product.get("ingredients_text") or "",
        "barcode": product.get("code") or "",
        "price": 0.0,
        "stock": 0,
        "source": "OpenFoodFacts"
    }


def fetch_product_details(query, timeout=10):
    query = str(query).strip()
    if not query:
        return None

    try:
        # Barcode search
        if query.isdigit():
            url = f"https://world.openfoodfacts.org/api/v2/product/{query}.json"
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            data = response.json()

            if data.get("status") != 1:
                return None

            product = data.get("product", {})
            return normalize_product(product)

        # Name search
        url = "https://world.openfoodfacts.org/cgi/search.pl"
        params = {
            "search_terms": query,
            "search_simple": 1,
            "action": "process",
            "json": 1,
            "page_size": 1
        }
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        data = response.json()

        products = data.get("products", [])
        if not products:
            return None

        return normalize_product(products[0])

    except requests.RequestException:
        return None