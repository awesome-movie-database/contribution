from dishka import Provider, Scope

from contribution.domain import (
    CreateMovie,
    UpdateMovie,
    CreateUser,
    UpdateUser,
    CreatePerson,
    UpdatePerson,
    CreateRole,
    UpdateRole,
    CreateWriter,
    UpdateWriter,
    CreateCrewMember,
    AddMovie,
    EditMovie,
    AddPerson,
    EditPerson,
    AcceptContribution,
    RejectContribution,
)


def domain_services_provider_factrory() -> Provider:
    provider = Provider(Scope.APP)

    provider.provide(CreateMovie)
    provider.provide(UpdateMovie)
    provider.provide(CreateUser)
    provider.provide(UpdateUser)
    provider.provide(CreatePerson)
    provider.provide(UpdatePerson)
    provider.provide(CreateRole)
    provider.provide(UpdateRole)
    provider.provide(CreateWriter)
    provider.provide(UpdateWriter)
    provider.provide(CreateCrewMember)
    provider.provide(AddMovie)
    provider.provide(EditMovie)
    provider.provide(AddPerson)
    provider.provide(EditPerson)
    provider.provide(AcceptContribution)
    provider.provide(RejectContribution)

    return provider
