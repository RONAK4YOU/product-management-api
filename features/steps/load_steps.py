"""Load each Gherkin table row through the running Product API."""
import os
import requests
from behave import given


@given("the product catalog contains")
def step_load_products(context):
    base_url = getattr(context, "base_url", os.getenv("PRODUCT_API_URL", "http://127.0.0.1:5000"))
    for row in context.table:
        payload = {
            "name": row["name"],
            "description": row["description"],
            "price": float(row["price"]),
            "available": row["available"].strip().lower() == "true",
            "category": row["category"],
        }
        response = requests.post(f"{base_url}/products", json=payload, timeout=10)
        assert response.status_code == 201, (
            f"Could not create {payload['name']}: {response.status_code} {response.text}"
        )
