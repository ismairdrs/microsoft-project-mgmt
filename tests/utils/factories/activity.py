from datetime import datetime

import factory
from faker import Factory as FakerFactory

from microsoft.app.models import DBActivity

faker = FakerFactory.create("pt_BR")


class DBAcivityFactory(factory.Factory):
    class Meta:
        model = DBActivity

    id = factory.LazyFunction(lambda: faker.uuid4())
    name = factory.LazyFunction(lambda: faker.name())
    description = factory.LazyFunction(lambda: faker.sentence())
    project_id = None
    created_at = factory.LazyFunction(lambda: datetime.now())
