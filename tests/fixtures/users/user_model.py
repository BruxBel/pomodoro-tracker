import factory.fuzzy
from faker import Faker
from pytest_factoryboy import register

from src.users.models import UserModel

fake = Faker()


@register(_name="user_model")
class UserModelFactory(factory.Factory):
    class Meta:
        model = UserModel

    id = factory.LazyFunction(lambda: fake.unique.random_int())
    username = factory.LazyFunction(lambda: fake.user_name())
    email = factory.LazyFunction(lambda: fake.email())
    name = factory.LazyFunction(lambda: fake.name())
    google_access_token = factory.LazyFunction(lambda: fake.sha256())
