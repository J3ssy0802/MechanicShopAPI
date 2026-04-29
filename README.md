# MechanicShop API

A RESTful Flask API for managing a mechanic shop — tracking customers, mechanics, and service tickets.

## Tech Stack

- **Flask** — web framework
- **Flask-SQLAlchemy** — ORM
- **Flask-Marshmallow / marshmallow-sqlalchemy** — serialization & validation
- **MySQL** — database (via `mysql-connector-python`)

## Prerequisites

- Python 3.10+
- MySQL server running locally

## Setup

1. **Clone the repository and navigate into it:**

   ```bash
   git clone <repo-url>
   cd MechanicShop
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create the MySQL database:**

   ```sql
   CREATE DATABASE mechanic_shop_db;
   ```

5. **Configure database credentials** in `config.py`:

   ```python
   SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://<user>:<password>@localhost/mechanic_shop_db'
   ```

6. **Run the app** (tables are auto-created on startup):

   ```bash
   python app.py
   ```

   The API will be available at `http://127.0.0.1:5000`.

7. **(Optional) Reset the database:**

   ```bash
   python reset_db.py
   ```

---

## API Endpoints

### Customers — `/customers`

| Method | Endpoint                  | Description           |
|--------|---------------------------|-----------------------|
| POST   | `/customers`              | Create a customer     |
| GET    | `/customers`              | Get all customers     |
| GET    | `/customers/<id>`         | Get customer by ID    |
| PUT    | `/customers/<id>`         | Update customer       |
| DELETE | `/customers/<id>`         | Delete customer       |

**Customer fields:** `name`, `email`, `password`

---

### Mechanics — `/mechanics`

| Method | Endpoint                  | Description           |
|--------|---------------------------|-----------------------|
| POST   | `/mechanics`              | Create a mechanic     |
| GET    | `/mechanics`              | Get all mechanics     |
| GET    | `/mechanics/<id>`         | Get mechanic by ID    |
| PUT    | `/mechanics/<id>`         | Update mechanic       |
| DELETE | `/mechanics/<id>`         | Delete mechanic       |

**Mechanic fields:** `name`, `email`, `phone`, `salary`

---

### Service Tickets — `/service_tickets`

| Method | Endpoint                                                    | Description                    |
|--------|-------------------------------------------------------------|--------------------------------|
| POST   | `/service_tickets`                                          | Create a service ticket        |
| GET    | `/service_tickets`                                          | Get all service tickets        |
| PUT    | `/service_tickets/<ticket_id>/assign_mechanic/<mechanic_id>` | Assign a mechanic to a ticket  |
| PUT    | `/service_tickets/<ticket_id>/remove_mechanic/<mechanic_id>` | Remove a mechanic from a ticket|

**Service ticket fields:** `customer_id`, `VIN`, `service_date`, `service_description`

---

## Project Structure

```
MechanicShop/
├── app.py                  # Entry point
├── config.py               # Configuration classes
├── requirements.txt
├── reset_db.py             # Drop and recreate all tables
└── app/
    ├── __init__.py         # App factory
    ├── extensions.py       # Marshmallow instance
    ├── models.py           # SQLAlchemy models
    └── blueprints/
        ├── customers/
        ├── mechanics/
        └── service_tickets/
```
