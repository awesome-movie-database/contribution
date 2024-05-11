from dishka import AsyncContainer, make_async_container

from .providers import (
    domain_validators_provider_factory,
    domain_services_provider_factrory,
)


def di_container_factory() -> AsyncContainer:
    di_container = make_async_container(
        domain_validators_provider_factory(),
        domain_services_provider_factrory(),
    )
    return di_container
