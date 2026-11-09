# Product Management API

A Flask and SQLite product catalog built for the ProductFactory CRUD and BDD assignment. Products have an ID, name, description, price, availability, and category. The project includes REST endpoints, a browser UI, a generated product factory, model and route tests, and Behave scenarios.

## Run locally

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`. The SQLite database is created automatically. The API starts empty; create products from the page or with `POST /products`.

## API endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/products` | Create a product |
| `GET` | `/products/{id}` | Read one product |
| `PUT` | `/products/{id}` | Update supplied product fields |
| `DELETE` | `/products/{id}` | Delete a product |
| `GET` | `/products` | List all products |
| `GET` | `/products?name=laptop` | Search by name |
| `GET` | `/products?category=Electronics` | Filter by category |
| `GET` | `/products?available=false` | Filter by availability |
| `GET` | `/health` | Health check |

Example JSON body:

```json
{
  "name": "Laptop Pro",
  "description": "Professional laptop",
  "price": 1299.99,
  "available": true,
  "category": "Electronics"
}
```

## Run tests

```powershell
pytest
```

To run the browser BDD scenarios, start the API with `python app.py` in one terminal, then run `behave` in another. Chrome and a compatible Selenium driver are required. Set `PRODUCT_API_URL` if the server uses a different URL.

## Assignment file map

- `tests/factories.py` — fake ProductFactory
- `tests/test_models.py` — model READ, UPDATE, DELETE, list, and filter tests
- `tests/test_routes.py` — API route tests
- `service/routes.py` — READ, UPDATE, DELETE, list, and filter endpoints
- `features/steps/load_steps.py` — BDD table data loader
- `features/products.feature` — CRUD and search scenarios
- `features/steps/web_steps.py` — Selenium button, results, and message steps
