from dishka import Provider, Scope

from contribution.application import UnitOfWork
from contribution.infrastructure.database import MongoDBUnitOfWork


def unit_of_work_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(MongoDBUnitOfWork, provides=UnitOfWork)

    return provider
