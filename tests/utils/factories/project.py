from datetime import datetime

import factory
from faker import Factory as FakerFactory

from microsoft.app.models import DBProject
from microsoft.enums import ProjectStatus

faker = FakerFactory.create("pt_BR")


class DBProjectFactory(factory.Factory):
    class Meta:
        model = DBProject

    id = factory.LazyFunction(lambda: faker.uuid4())
    name = factory.LazyFunction(lambda: faker.name())
    description = factory.LazyFunction(lambda: faker.sentence())
    status = ProjectStatus.OPEN
    client_id = None
    created_at = factory.LazyFunction(lambda: datetime.now())
