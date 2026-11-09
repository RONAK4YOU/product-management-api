from service.models import Product
from tests.factories import ProductFactory


def test_read_product():
    product = ProductFactory(name="Sample Product", description="Test description").create()
    found = Product.find(product.id)
    assert found is not None
    assert found.id == product.id
    assert found.name == product.name


def test_update_product():
    product = ProductFactory(name="Sample Product", description="Original description").create()
    original_id = product.id
    product.description = "Updated product description"
    product.update()
    updated = Product.find(original_id)
    assert updated.id == original_id
    assert updated.description == "Updated product description"


def test_delete_product(app):
    with app.app_context():
        product = ProductFactory().create()
        assert Product.query.count() == 1
        product.delete()
        assert Product.query.count() == 0


def test_list_all_products():
    assert Product.all() == []
    created = ProductFactory.create_batch(4)
    for product in created:
        product.create()
    listed = Product.all()
    assert len(listed) == len(created)
    assert {p.id for p in listed} == {p.id for p in created}


def test_find_products_by_name():
    matches = ProductFactory.create_batch(3, name="Matching Product")
    others = ProductFactory.create_batch(2, name="Different Product")
    for product in matches + others:
        product.create()
    search_name = matches[0].name
    results = Product.find_by_name(search_name)
    assert len(results) == len(matches)
    assert all(product.name == search_name for product in results)


def test_find_products_by_category():
    matches = ProductFactory.create_batch(3, category="Electronics")
    others = ProductFactory.create_batch(2, category="Home")
    for product in matches + others:
        product.create()
    category = matches[0].category
    expected_count = len(matches)
    results = Product.find_by_category(category)
    assert len(results) == expected_count
    assert all(product.category == category for product in results)


def test_find_products_by_availability():
    matches = ProductFactory.create_batch(3, available=False)
    others = ProductFactory.create_batch(2, available=True)
    for product in matches + others:
        product.create()
    availability = matches[0].available
    results = Product.find_by_availability(availability)
    assert len(results) == len(matches)
    assert all(product.available is availability for product in results)
