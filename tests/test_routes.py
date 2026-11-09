from service.models import Product
from tests.factories import ProductFactory


def payload(**overrides):
    product = ProductFactory()
    data = product.serialize()
    data.pop("id", None)
    data.update(overrides)
    return data


def create_product(client, **overrides):
    response = client.post("/products", json=payload(**overrides))
    assert response.status_code == 201
    return response.json


def test_read_product(client):
    product = create_product(client, name="Readable Product", description="Read test")
    response = client.get(f"/products/{product['id']}")
    assert response.status_code == 200
    assert response.json["id"] == product["id"]
    assert response.json["name"] == product["name"]


def test_update_product(client):
    product = create_product(client, description="Original description")
    response = client.put(
        f"/products/{product['id']}",
        json={"description": "Updated description"},
    )
    assert response.status_code == 200
    assert response.json["id"] == product["id"]
    assert response.json["description"] == "Updated description"


def test_delete_product(client):
    product = create_product(client)
    count_before_delete = Product.query.count()
    response = client.delete(f"/products/{product['id']}")
    assert response.status_code == 204
    assert response.data == b""
    assert Product.query.count() == count_before_delete - 1
    assert client.get(f"/products/{product['id']}").status_code == 404


def test_list_all_products(client):
    products_to_create = [payload(name=f"Test Product {i}") for i in range(5)]
    for product_data in products_to_create:
        response = client.post("/products", json=product_data)
        assert response.status_code == 201
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json["count"] == len(products_to_create)
    assert len(response.json["products"]) == len(products_to_create)


def test_list_by_name(client):
    create_product(client, name="Laptop Pro")
    create_product(client, name="Desk Lamp")
    response = client.get("/products?name=Laptop")
    assert response.status_code == 200
    assert response.json["count"] == 1
    assert response.json["products"][0]["name"] == "Laptop Pro"


def test_list_by_category(client):
    create_product(client, name="Laptop", category="Electronics")
    create_product(client, name="Headphones", category="Electronics")
    create_product(client, name="Lamp", category="Home")
    response = client.get("/products?category=Electronics")
    assert response.status_code == 200
    assert response.json["count"] == 2
    assert all(p["category"] == "Electronics" for p in response.json["products"])


def test_list_by_availability(client):
    create_product(client, name="Unavailable Headphones", available=False)
    create_product(client, name="Available Laptop", available=True)
    response = client.get("/products?available=false")
    assert response.status_code == 200
    assert response.json["count"] == 1
    assert response.json["products"][0]["available"] is False

