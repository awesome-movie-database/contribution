from dishka import Provider, Scope

from contribution.domain.services import (
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

    provider.provide(CreateMovie, provides=CreateMovie)
    provider.provide(UpdateMovie, provides=UpdateMovie)
    provider.provide(CreateUser, provides=CreateUser)
    provider.provide(UpdateUser, provides=UpdateUser)
    provider.provide(CreatePerson, provides=CreatePerson)
    provider.provide(UpdatePerson, provides=UpdatePerson)
    provider.provide(CreateRole, provides=CreateRole)
    provider.provide(UpdateRole, provides=UpdateRole)
    provider.provide(CreateWriter, provides=CreateWriter)
    provider.provide(UpdateWriter, provides=UpdateWriter)
    provider.provide(CreateCrewMember, provides=CreateCrewMember)
    provider.provide(AddMovie, provides=AddMovie)
    provider.provide(EditMovie, provides=EditMovie)
    provider.provide(AddPerson, provides=AddPerson)
    provider.provide(EditPerson, provides=EditPerson)
    provider.provide(AcceptContribution, provides=AcceptContribution)
    provider.provide(RejectContribution, provides=RejectContribution)

    return provider
