from flask import Flask, jsonify, request

from inventory import (
    get_all_items,
    get_item,
    add_item,
    update_item,
    delete_item
)
from openfood import fetch_product_details

app = Flask(__name__)


def error_response(message, status_code):
    return jsonify({"error": message}), status_code


def validate_create_payload(data):
    required_fields = ["product_name", "brands", "price", "stock"]
    missing = [field for field in required_fields if data.get(field) in [None, ""]]

    if missing:
        return None, f"Missing required field(s): {', '.join(missing)}"

    try:
        price = float(data["price"])
    except (TypeError, ValueError):
        return None, "price must be a number"

    try:
        stock = int(data["stock"])
    except (TypeError, ValueError):
        return None, "stock must be an integer"

    item = {
        "product_name": data["product_name"],
        "brands": data["brands"],
        "ingredients_text": data.get("ingredients_text", ""),
        "barcode": data.get("barcode", ""),
        "price": price,
        "stock": stock,
        "source": data.get("source", "local")
    }
    return item, None


@app.get("/")
def home():
    return jsonify({"message": "Inventory API is running"}), 200


@app.get("/inventory")
def get_inventory():
    return jsonify(get_all_items()), 200


@app.get("/inventory/<int:item_id>")
def get_inventory_item(item_id):
    item = get_item(item_id)
    if not item:
        return error_response("Item not found", 404)
    return jsonify(item), 200


@app.post("/inventory")
def create_inventory_item():
    data = request.get_json(silent=True) or {}
    item, err = validate_create_payload(data)

    if err:
        return error_response(err, 400)

    created = add_item(item)
    return jsonify(created), 201


@app.patch("/inventory/<int:item_id>")
def patch_inventory_item(item_id):
    existing = get_item(item_id)
    if not existing:
        return error_response("Item not found", 404)

    data = request.get_json(silent=True) or {}
    updates = {}

    if "product_name" in data and data["product_name"] != "":
        updates["product_name"] = str(data["product_name"])

    if "brands" in data and data["brands"] != "":
        updates["brands"] = str(data["brands"])

    if "ingredients_text" in data:
        updates["ingredients_text"] = str(data["ingredients_text"])

    if "barcode" in data:
        updates["barcode"] = str(data["barcode"])

    if "source" in data:
        updates["source"] = str(data["source"])

    if "price" in data:
        try:
            updates["price"] = float(data["price"])
        except (TypeError, ValueError):
            return error_response("price must be a number", 400)

    if "stock" in data:
        try:
            updates["stock"] = int(data["stock"])
        except (TypeError, ValueError):
            return error_response("stock must be an integer", 400)

    if not updates:
        return error_response("No valid fields provided for update", 400)

    updated = update_item(item_id, updates)
    return jsonify(updated), 200


@app.delete("/inventory/<int:item_id>")
def remove_inventory_item(item_id):
    deleted = delete_item(item_id)
    if not deleted:
        return error_response("Item not found", 404)

    return jsonify({
        "message": "Item deleted successfully",
        "deleted": deleted
    }), 200


@app.get("/openfoodfacts/search")
def search_openfoodfacts():
    query = request.args.get("query", "").strip()
    if not query:
        return error_response("query parameter is required", 400)

    product = fetch_product_details(query)
    if not product:
        return error_response("Product not found in OpenFoodFacts", 404)

    return jsonify(product), 200


@app.post("/inventory/import")
def import_from_openfoodfacts():
    data = request.get_json(silent=True) or {}
    query = data.get("query") or data.get("barcode")

    if not query:
        return error_response("query or barcode is required", 400)

    product = fetch_product_details(query)
    if not product:
        return error_response("Product not found in OpenFoodFacts", 404)

    if "price" in data:
        try:
            product["price"] = float(data["price"])
        except (TypeError, ValueError):
            return error_response("price must be a number", 400)

    if "stock" in data:
        try:
            product["stock"] = int(data["stock"])
        except (TypeError, ValueError):
            return error_response("stock must be an integer", 400)

    created = add_item(product)
    return jsonify(created), 201


if __name__ == "__main__":
    app.run(debug=True,port=5001)