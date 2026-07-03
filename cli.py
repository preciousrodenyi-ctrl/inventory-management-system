import requests

BASE_URL = "http://127.0.0.1:5001"


def view_inventory():
    response = requests.get(f"{BASE_URL}/inventory")

    if response.status_code == 200:
        inventory = response.json()

        print("\n===== INVENTORY =====")

        for item in inventory:
            print(f"""
ID: {item['id']}
Name: {item['name']}
Brand: {item['brand']}
Price: ${item['price']}
Stock: {item['stock']}
Barcode: {item['barcode']}
----------------------------
""")
    else:
        print("Error retrieving inventory.")


def add_product():
    print("\n=== Add Product ===")

    product = {
        "id": int(input("ID: ")),
        "name": input("Name: "),
        "brand": input("Brand: "),
        "price": float(input("Price: ")),
        "stock": int(input("Stock: ")),
        "barcode": input("Barcode: "),
        "ingredients": input("Ingredients: ")
    }

    response = requests.post(
        f"{BASE_URL}/inventory",
        json=product
    )

    print(response.json())


def update_product():
    print("\n=== Update Product ===")

    item_id = int(input("Enter Product ID: "))

    price = float(input("New Price: "))
    stock = int(input("New Stock: "))

    response = requests.patch(
        f"{BASE_URL}/inventory/{item_id}",
        json={
            "price": price,
            "stock": stock
        }
    )

    print(response.json())


def delete_product():
    print("\n=== Delete Product ===")

    item_id = int(input("Enter Product ID: "))

    response = requests.delete(
        f"{BASE_URL}/inventory/{item_id}"
    )

    print(response.json())


def search_openfood():
    print("\n=== Search OpenFoodFacts ===")

    barcode = input("Enter barcode: ")

    response = requests.get(
        f"{BASE_URL}/openfood/{barcode}"
    )

    print(response.json())


def menu():

    while True:

        print("""
=========================
Inventory Management CLI
=========================

1. View Inventory

2. Add Product

3. Update Product

4. Delete Product

5. Search OpenFoodFacts

6. Exit

=========================
""")

        choice = input("Choose an option: ")

        if choice == "1":
            view_inventory()

        elif choice == "2":
            add_product()

        elif choice == "3":
            update_product()

        elif choice == "4":
            delete_product()

        elif choice == "5":
            search_openfood()

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    menu()