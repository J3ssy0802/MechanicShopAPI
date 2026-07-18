# MechanicShop API

REST API for a mechanic shop built with Flask, SQLAlchemy, and Marshmallow

## What Is Included

- Customer management
- Mechanic management
- Service ticket management
- Inventory management
- Ticket assignments for mechanics and inventory items
- JWT token utility + token-protected customer routes
- Rate limiting support via Flask-Limiter
- Caching support via Flask-Caching
- OpenAPI/Swagger documentation via Swagger UI
- Unit tests for customers, mechanics, inventory, and service tickets

## Tech Stack

- Flask
- Flask-SQLAlchemy
- flask-marshmallow + marshmallow-sqlalchemy
- Flask-Limiter
- Flask-Caching
- python-jose (JWT)
- MySQL (mysql-connector-python)

## Prerequisites

- Python 3.10+
- MySQL server

## Setup

1. Clone the repo and enter the folder.

```bash
git clone <repo-url>
cd MechanicShop
```

2. Create and activate a virtual environment.

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Create the database in MySQL.

```sql
CREATE DATABASE mechanic_shop_db;
```

5. Update DB credentials in `config.py`.

```python
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://<user>:<password>@localhost/mechanic_shop_db"
```

6. Run the app.

```bash
python app.py
```

API base URL: `http://127.0.0.1:5000`

7. Optional: reset tables.

```bash
python reset_db.py
```

## Testing

The project uses Python's built-in `unittest` test runner.

Run the full test suite:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

Run a single test module:

```bash
python -m unittest tests.test_customer
python -m unittest tests.test_mechanic
python -m unittest tests.test_inventory
python -m unittest tests.test_service_tickets
```

Current test files:

- `tests/test_customer.py`
- `tests/test_mechanic.py`
- `tests/test_inventory.py`
- `tests/test_service_tickets.py`

Testing uses `TestingConfig` (SQLite: `sqlite:///testing.db`) from `config.py`.

## Authentication

Token-protected routes use an `Authorization` header with bearer token format:

```http
Authorization: Bearer <jwt_token>
```

Current customer routes decorated with `@token_required`:

- `PUT /customers/`
- `DELETE /customers/`
- `GET /customers/my-tickets`

## API Documentation

Swagger UI is available when the app is running:

- UI: `http://127.0.0.1:5000/api/docs`
- OpenAPI file: `app/static/swagger.yaml`

You can also import and use the included Postman collection:

- `MechanicShop.postman_collection.json`

## API Endpoints

### Customers (`/customers`)

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/customers` | Create customer |
| GET | `/customers` | List customers (supports optional `page` and `per_page` query params) |
| GET | `/customers/<customer_id>` | Get customer by id |
| PUT | `/customers/` | Update authenticated customer (token required) |
| POST | `/customers/login` | Customer login |
| DELETE | `/customers/` | Delete authenticated customer (token required) |
| GET | `/customers/my-tickets` | Get authenticated customer tickets (token required) |

Customer fields:

- `name`
- `email`
- `password`

### Mechanics (`/mechanics`)

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/mechanics` | Create mechanic |
| GET | `/mechanics` | List mechanics |
| GET | `/mechanics/most-tickets` | List mechanics sorted by ticket count desc |
| GET | `/mechanics/<mechanic_id>` | Get mechanic by id |
| PUT | `/mechanics/<mechanic_id>` | Update mechanic |
| DELETE | `/mechanics/<mechanic_id>` | Delete mechanic |

Mechanic fields:

- `name`
- `email`
- `phone`
- `salary`

### Service Tickets (`/service_tickets`)

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/service_tickets` | Create service ticket |
| GET | `/service_tickets` | List all service tickets |
| PUT | `/service_tickets/<ticket_id>/assign_mechanic/<mechanic_id>` | Assign mechanic to ticket |
| PUT | `/service_tickets/<ticket_id>/update_mechanics` | Add/remove mechanics in one request |
| PUT | `/service_tickets/<ticket_id>/assign_inventory/<inventory_id>` | Assign inventory item to ticket |

Service ticket fields:

- `customer_id`
- `VIN`
- `service_date`
- `service_description`

Update mechanics payload:

```json
{
  "add_mechanic_id": [1, 2],
  "remove_mechanic_id": [3]
}
```

### Inventory (`/inventory`)

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/inventory` | Create inventory item |
| GET | `/inventory` | List inventory items |
| GET | `/inventory/<inventory_id>` | Get inventory item by id |
| PUT | `/inventory/<inventory_id>` | Update inventory item |
| DELETE | `/inventory/<inventory_id>` | Delete inventory item |

Inventory fields:

- `name`
- `price`

## Data Model Overview

- `Customer` has many `service_ticket`
- `Mechanic` many-to-many with `service_ticket`
- `Inventory` many-to-many with `service_ticket`
- Join tables:
  - `service_ticket_mechanic`
  - `service_ticket_inventory`

## Project Structure

```text
MechanicShop/
|-- app.py
|-- config.py
|-- reset_db.py
|-- requirements.txt
|-- MechanicShop.postman_collection.json
|-- app/
|   |-- __init__.py
|   |-- extensions.py
|   |-- models.py
|   |-- blueprints/
|   |   |-- customers/
|   |   |   |-- __init__.py
|   |   |   |-- routes.py
|   |   |   `-- schemas.py
|   |   |-- mechanics/
|   |   |   |-- __init__.py
|   |   |   |-- routes.py
|   |   |   `-- schemas.py
|   |   |-- service_tickets/
|   |   |   |-- __init__.py
|   |   |   |-- routes.py
|   |   |   `-- schemas.py
|   |   `-- inventory/
|   |       |-- __init__.py
|   |       |-- routes.py
|   |       `-- schemas.py
|   `-- utils/
|       `-- util.py
`-- README.md
```

## Deploying To Render

Use these settings when creating a Render Web Service for this project:

- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn flask_app:app`
- Health Check Path: `/healthz`

### Required Environment Variables

Set the following environment variable in Render:

- `SQLALCHEMY_DATABASE_URI`

Example (Render Postgres connection string):

```text
postgresql+psycopg2://<user>:<password>@<host>:<port>/<database>
```

### Why These Settings

- The app exposes both `/` and `/healthz` endpoints that return HTTP 200 for health checks.
- `gunicorn flask_app:app` imports the Flask app object without running the local development server.
- The app reads `PORT` automatically in `flask_app.py` when run directly.

## Notes

- `db.create_all()` runs on app startup in `app.py`.
- A Postman collection is included in `MechanicShop.postman_collection.json`.
