# Inventory Management System

## Project Overview

This project is a Flask-based REST API for managing inventory in a small retail business. It allows users to create, read, update, and delete inventory items while also integrating with the OpenFoodFacts API to retrieve product information by barcode.

The project also includes a Command Line Interface (CLI) for interacting with the API and a comprehensive test suite built with pytest.

---

## Features

* Flask REST API
* CRUD Operations

  * View all inventory items
  * View a single inventory item
  * Add new inventory items
  * Update existing inventory items
  * Delete inventory items
* OpenFoodFacts API integration
* Command Line Interface (CLI)
* Unit testing using pytest
* Mock testing using unittest.mock
* Git version control

---

## Project Structure

```text
inventory-management-system/
│
├── app.py
├── inventory.py
├── openfood.py
├── cli.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── tests/
    ├── test_api.py
    ├── test_cli.py
    └── test_openfood.py
```

---

## Requirements

* Python 3.10 or later
* Flask
* Requests
* Pytest

---

## Installation

### Clone the repository

```bash
git clone https://github.com/preciousrodenyi-ctrl/inventory-management-system.git
```

### Enter the project folder

```bash
cd inventory-management-system
```

### Create a virtual environment

Linux/macOS

```bash
python3 -m venv venv
```

Windows

```bash
python -m venv venv
```

---

### Activate the virtual environment

Linux/macOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

---

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Flask API

Start the Flask application:

```bash
python app.py
```

The API runs at:

```text
http://127.0.0.1:5000
```

---

## Running the CLI

Open a second terminal and run:

```bash
python cli.py
```

Make sure the Flask server is running before starting the CLI.

---

## API Endpoints

| Method | Endpoint           | Description                     |
| ------ | ------------------ | ------------------------------- |
| GET    | /                  | API information                 |
| GET    | /inventory         | Get all inventory items         |
| GET    | /inventory/<id>    | Get a single inventory item     |
| POST   | /inventory         | Create a new inventory item     |
| PATCH  | /inventory/<id>    | Update an inventory item        |
| DELETE | /inventory/<id>    | Delete an inventory item        |
| GET    | /product/<barcode> | Search OpenFoodFacts by barcode |

---

## Example JSON Request

POST `/inventory`

```json
{
    "barcode": "123456789",
    "product_name": "Milk",
    "brand": "Brookside",
    "price": 200,
    "stock": 30
}
```

---

## Example JSON Response

```json
{
    "message": "Item added successfully",
    "item": {
        "id": 3,
        "barcode": "123456789",
        "product_name": "Milk",
        "brand": "Brookside",
        "price": 200,
        "stock": 30
    }
}
```

---

## Running Tests

Run all tests:

```bash
pytest
```

Run API tests only:

```bash
pytest tests/test_api.py
```

Run CLI tests only:

```bash
pytest tests/test_cli.py
```

Run OpenFoodFacts tests only:

```bash
pytest tests/test_openfood.py
```

---

## Technologies Used

* Python
* Flask
* Requests
* Pytest
* unittest.mock
* Git
* GitHub
* OpenFoodFacts API

---

## Future Improvements

* SQLite or PostgreSQL database
* User authentication
* Product image support
* Search by product name
* Pagination
* Docker support
* Deployment to Render or Railway

---

## Author

Precious faith

Python REST API Inventory Management System

Summative Lab Project
