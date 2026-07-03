from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Mock database array seeded with OpenFoodFacts-style data
inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "price": 3.99,
        "stock": 45
    },
    {
        "id": 2,
        "product_name": "Dark Chocolate 70%",
        "brands": "Lindt",
        "ingredients_text": "Cocoa mass, sugar, cocoa butter",
        "price": 2.49,
        "stock": 120
    }
]
current_id = 3

# Helper function to fetch data from OpenFoodFacts API
def fetch_from_openfoodfacts(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 1:
                prod = data.get("product", {})
                return {
                    "product_name": prod.get("product_name", "Unknown Product"),
                    "brands": prod.get("brands", "Unknown Brand"),
                    "ingredients_text": prod.get("ingredients_text", "No ingredients provided")
                }
    except requests.RequestException:
        pass
    return None

# --- API ROUTES ---

@app.route('/inventory', methods=['GET'])
def get_all_items():
    return jsonify(inventory), 200

@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

@app.route('/inventory', methods=['POST'])
def add_item():
    global current_id
    data = request.get_json() or {}
    
    # Check if we need to fetch data via external barcode API
    barcode = data.get("barcode")
    if barcode:
        external_data = fetch_from_openfoodfacts(barcode)
        if external_data:
            data.update(external_data)
            
    if "product_name" not in data:
        return jsonify({"error": "Missing required field: product_name"}), 400
        
    new_item = {
        "id": current_id,
        "product_name": data.get("product_name"),
        "brands": data.get("brands", "Generic"),
        "ingredients_text": data.get("ingredients_text", "N/A"),
        "price": float(data.get("price", 0.0)),
        "stock": int(data.get("stock", 0))
    }
    inventory.append(new_item)
    current_id += 1
    return jsonify(new_item), 201

@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
        
    data = request.get_json() or {}
    if "price" in data:
        item["price"] = float(data["price"])
    if "stock" in data:
        item["stock"] = int(data["stock"])
    if "product_name" in data:
        item["product_name"] = data["product_name"]
        
    return jsonify(item), 200

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global inventory
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    inventory = [i for i in inventory if i["id"] != item_id]
    return jsonify({"message": "Item successfully deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)