from dishka import AsyncContainer, make_async_container

from .providers import (
    cli_configs_provider_factory,
    web_api_configs_provider_factory,
    domain_validators_provider_factory,
    domain_services_provider_factrory,
    motor_provider_factory,
    redis_provider_factory,
    aioboto3_provider_factory,
    aio_pika_provider_factory,
    identity_maps_provider_factory,
    collections_provider_factory,
    collection_committers_provider_factory,
    mongodb_lock_factory_provider_factory,
    unit_of_work_provider_factory,
    data_mappers_provider_factory,
    cache_provider_factory,
    permissions_storage_provider_factory,
    photo_storage_provider_factory,
    fastapi_request_provider_factory,
    web_api_identity_provider_provider_factory,
    cli_operation_id_provider_factory,
    web_api_operation_id_provider_factory,
    event_publishers_provider_factory,
    application_services_provider_factory,
    cli_command_processors_provider_factory,
    web_api_command_processors_provider_factory,
)


def cli_ioc_container_factory() -> AsyncContainer:
    ioc_container = make_async_container(
        cli_configs_provider_factory(),
        domain_validators_provider_factory(),
        domain_services_provider_factrory(),
        motor_provider_factory(),
        identity_maps_provider_factory(),
        collections_provider_factory(),
        collection_committers_provider_factory(),
        mongodb_lock_factory_provider_factory(),
        unit_of_work_provider_factory(),
        data_mappers_provider_factory(),
        cli_operation_id_provider_factory(),
        application_services_provider_factory(),
        cli_command_processors_provider_factory(),
    )
    return ioc_container


def web_api_ioc_container_factory() -> AsyncContainer:
    ioc_container = make_async_container(
        web_api_configs_provider_factory(),
        domain_validators_provider_factory(),
        domain_services_provider_factrory(),
        motor_provider_factory(),
        redis_provider_factory(),
        aioboto3_provider_factory(),
        aio_pika_provider_factory(),
        identity_maps_provider_factory(),
        collections_provider_factory(),
        collection_committers_provider_factory(),
        mongodb_lock_factory_provider_factory(),
        unit_of_work_provider_factory(),
        data_mappers_provider_factory(),
        cache_provider_factory(),
        permissions_storage_provider_factory(),
        photo_storage_provider_factory(),
        fastapi_request_provider_factory(),
        web_api_identity_provider_provider_factory(),
        web_api_operation_id_provider_factory(),
        event_publishers_provider_factory(),
        application_services_provider_factory(),
        web_api_command_processors_provider_factory(),
    )
    return ioc_container
