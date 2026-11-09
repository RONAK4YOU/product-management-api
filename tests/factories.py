"""factory_boy factory that generates complete fake Product records."""
import factory
from service.models import Product


class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    id = factory.Sequence(lambda number: number + 1)
    name = factory.Faker("catch_phrase")
    description = factory.Faker("sentence")
    price = factory.Faker("pyfloat", min_value=1, max_value=9999, right_digits=2)
    available = factory.Faker("pybool")
    category = factory.Faker("word")
