from flask import Flask, jsonify, request, render_template

from inventory import (
    get_all_items,
    get_item,
    add_item,
    update_item,
    delete_item
)

from openfood import get_product_by_barcode

app = Flask(__name__)


# -----------------------
# Home Page
# -----------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------
# Get all inventory
# -----------------------
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(get_all_items())


# -----------------------
# Get one item
# -----------------------
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_single_item(item_id):

    item = get_item(item_id)

    if item:
        return jsonify(item)

    return jsonify({"error": "Item not found"}), 404


# -----------------------
# Add item
# -----------------------
@app.route("/inventory", methods=["POST"])
def create_item():

    data = request.get_json()

    add_item(data)

    return jsonify({
        "message": "Product added successfully",
        "product": data
    }), 201


# -----------------------
# Update item
# -----------------------
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def patch_item(item_id):

    data = request.get_json()

    item = update_item(item_id, data)

    if item:
        return jsonify(item)

    return jsonify({"error": "Item not found"}), 404


# -----------------------
# Delete item
# -----------------------
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def remove_item(item_id):

    if delete_item(item_id):
        return jsonify({"message": "Deleted successfully"})

    return jsonify({"error": "Item not found"}), 404


# -----------------------
# OpenFoodFacts
# -----------------------
@app.route("/openfood/<barcode>", methods=["GET"])
def openfood(barcode):

    product = get_product_by_barcode(barcode)

    if product:
        return jsonify(product)

    return jsonify({"error": "Product not found"}), 404


# -----------------------
# Run Flask
# -----------------------
if __name__ == "__main__":
    app.run(debug=True, port=5001)