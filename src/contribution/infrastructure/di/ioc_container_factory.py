from dishka import AsyncContainer, make_async_container

from .providers import (
    configs_provider_factory,
    domain_validators_provider_factory,
    domain_services_provider_factrory,
    motor_provider_factory,
    redis_provider_factory,
    aioboto3_provider_factory,
    identity_maps_provider_factory,
    collections_provider_factory,
    data_mappers_provider_factory,
    cache_provider_factory,
    permissions_storage_provider_factory,
    photo_storage_provider_factory,
    identity_provider_provider_factory,
    application_services_provider_factory,
    command_processors_provider_factory,
)


def ioc_container_factory() -> AsyncContainer:
    ioc_container = make_async_container(
        configs_provider_factory(),
        domain_validators_provider_factory(),
        domain_services_provider_factrory(),
        motor_provider_factory(),
        redis_provider_factory(),
        aioboto3_provider_factory(),
        identity_maps_provider_factory(),
        collections_provider_factory(),
        data_mappers_provider_factory(),
        cache_provider_factory(),
        permissions_storage_provider_factory(),
        photo_storage_provider_factory(),
        identity_provider_provider_factory(),
        application_services_provider_factory(),
        command_processors_provider_factory(),
    )
    return ioc_container
