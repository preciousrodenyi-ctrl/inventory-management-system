inventory = [
    {
        "id": 1,
        "name": "Organic Almond Milk",
        "brand": "Silk",
        "price": 5.99,
        "stock": 20,
        "barcode": "737628064502",
        "ingredients": "Filtered water, almonds, cane sugar"
    },
    {
        "id": 2,
        "name": "Whole Wheat Bread",
        "brand": "Nature's Own",
        "price": 3.50,
        "stock": 15,
        "barcode": "1234567890123",
        "ingredients": "Whole wheat flour, water, yeast"
    }
]


def get_all_items():
    return inventory


def get_item(item_id):
    return next((item for item in inventory if item["id"] == item_id), None)


def add_item(item):
    inventory.append(item)
    return item


def update_item(item_id, data):
    item = get_item(item_id)

    if item:
        item.update(data)
        return item

    return None


def delete_item(item_id):
    item = get_item(item_id)

    if item:
        inventory.remove(item)
        return True

    return False