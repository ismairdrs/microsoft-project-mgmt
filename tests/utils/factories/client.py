from datetime import datetime

import factory
from faker import Factory as FakerFactory

from microsoft.app.models import DBClient

faker = FakerFactory.create("pt_BR")


class DBClientFactory(factory.Factory):
    class Meta:
        model = DBClient

    id = factory.LazyFunction(lambda: faker.uuid4())
    name = factory.LazyFunction(lambda: faker.name())
    email = factory.LazyFunction(lambda: faker.email())
    phone = factory.LazyFunction(lambda: faker.phone_number())
    created_at = factory.LazyFunction(lambda: datetime.now())
