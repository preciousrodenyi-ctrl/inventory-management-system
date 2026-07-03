import argparse
import json
import os
import requests

BASE_URL = os.getenv("INVENTORY_API_URL", "http://127.0.0.1:5001")


def pretty_print(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


def make_request(method, path, **kwargs):
    url = f"{BASE_URL}{path}"
    try:
        response = getattr(requests, method)(url, timeout=10, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        print(f"Request failed: {exc}")
        return None
    except ValueError:
        print("Invalid JSON response")
        return None


def cmd_list(args):
    data = make_request("get", "/inventory")
    if data is not None:
        pretty_print(data)


def cmd_get(args):
    data = make_request("get", f"/inventory/{args.id}")
    if data is not None:
        pretty_print(data)


def cmd_add(args):
    payload = {
        "product_name": args.name,
        "brands": args.brand,
        "ingredients_text": args.ingredients or "",
        "barcode": args.barcode or "",
        "price": args.price,
        "stock": args.stock,
        "source": "local"
    }
    data = make_request("post", "/inventory", json=payload)
    if data is not None:
        pretty_print(data)


def cmd_update(args):
    payload = {}
    if args.name is not None:
        payload["product_name"] = args.name
    if args.brand is not None:
        payload["brands"] = args.brand
    if args.ingredients is not None:
        payload["ingredients_text"] = args.ingredients
    if args.barcode is not None:
        payload["barcode"] = args.barcode
    if args.price is not None:
        payload["price"] = args.price
    if args.stock is not None:
        payload["stock"] = args.stock

    data = make_request("patch", f"/inventory/{args.id}", json=payload)
    if data is not None:
        pretty_print(data)


def cmd_delete(args):
    data = make_request("delete", f"/inventory/{args.id}")
    if data is not None:
        pretty_print(data)


def cmd_search(args):
    data = make_request("get", f"/openfoodfacts/search?query={args.query}")
    if data is not None:
        pretty_print(data)


def cmd_import(args):
    payload = {}
    if args.query:
        payload["query"] = args.query
    if args.barcode:
        payload["barcode"] = args.barcode
    if args.price is not None:
        payload["price"] = args.price
    if args.stock is not None:
        payload["stock"] = args.stock

    data = make_request("post", "/inventory/import", json=payload)
    if data is not None:
        pretty_print(data)


def build_parser():
    parser = argparse.ArgumentParser(description="Inventory Management CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List all inventory items")
    list_parser.set_defaults(func=cmd_list)

    get_parser = subparsers.add_parser("get", help="Get one inventory item")
    get_parser.add_argument("id", type=int)
    get_parser.set_defaults(func=cmd_get)

    add_parser = subparsers.add_parser("add", help="Add an inventory item")
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--brand", required=True)
    add_parser.add_argument("--ingredients", default="")
    add_parser.add_argument("--barcode", default="")
    add_parser.add_argument("--price", type=float, required=True)
    add_parser.add_argument("--stock", type=int, required=True)
    add_parser.set_defaults(func=cmd_add)

    update_parser = subparsers.add_parser("update", help="Update an inventory item")
    update_parser.add_argument("id", type=int)
    update_parser.add_argument("--name")
    update_parser.add_argument("--brand")
    update_parser.add_argument("--ingredients")
    update_parser.add_argument("--barcode")
    update_parser.add_argument("--price", type=float)
    update_parser.add_argument("--stock", type=int)
    update_parser.set_defaults(func=cmd_update)

    delete_parser = subparsers.add_parser("delete", help="Delete an inventory item")
    delete_parser.add_argument("id", type=int)
    delete_parser.set_defaults(func=cmd_delete)

    search_parser = subparsers.add_parser("search", help="Search OpenFoodFacts")
    search_parser.add_argument("query")
    search_parser.set_defaults(func=cmd_search)

    import_parser = subparsers.add_parser("import", help="Import item from OpenFoodFacts into inventory")
    import_parser.add_argument("--query")
    import_parser.add_argument("--barcode")
    import_parser.add_argument("--price", type=float)
    import_parser.add_argument("--stock", type=int)
    import_parser.set_defaults(func=cmd_import)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()