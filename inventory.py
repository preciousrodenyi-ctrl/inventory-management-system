from copy import deepcopy

DEFAULT_INVENTORY = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "barcode": "1234567890123",
        "price": 3.99,
        "stock": 25,
        "source": "local"
    },
    {
        "id": 2,
        "product_name": "Oat Milk",
        "brands": "Oatly",
        "ingredients_text": "Water, oats, salt",
        "barcode": "2345678901234",
        "price": 4.49,
        "stock": 18,
        "source": "local"
    },
    {
        "id": 3,
        "product_name": "Peanut Butter",
        "brands": "Jif",
        "ingredients_text": "Roasted peanuts, sugar, palm oil",
        "barcode": "3456789012345",
        "price": 2.89,
        "stock": 40,
        "source": "local"
    }
]

INVENTORY = deepcopy(DEFAULT_INVENTORY)
NEXT_ID = max(item["id"] for item in INVENTORY) + 1 if INVENTORY else 1


def reset_store(seed=None):
    global INVENTORY, NEXT_ID
    INVENTORY = deepcopy(seed if seed is not None else DEFAULT_INVENTORY)
    NEXT_ID = max([item["id"] for item in INVENTORY], default=0) + 1


def get_all_items():
    return deepcopy(INVENTORY)


def get_item(item_id):
    for item in INVENTORY:
        if item["id"] == item_id:
            return deepcopy(item)
    return None


def add_item(item):
    global NEXT_ID
    new_item = deepcopy(item)
    new_item["id"] = NEXT_ID
    NEXT_ID += 1
    INVENTORY.append(new_item)
    return deepcopy(new_item)


def update_item(item_id, updates):
    for index, item in enumerate(INVENTORY):
        if item["id"] == item_id:
            INVENTORY[index].update(updates)
            return deepcopy(INVENTORY[index])
    return None


def delete_item(item_id):
    for index, item in enumerate(INVENTORY):
        if item["id"] == item_id:
            removed = INVENTORY.pop(index)
            return deepcopy(removed)
    return None