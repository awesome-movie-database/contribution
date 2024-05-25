from dishka import Provider, Scope

from contribution.domain import (
    ValidateMovieEngTitle,
    ValidateMovieOriginalTitle,
    ValidateMovieDuration,
    ValidateUserName,
    ValidatePersonFirstName,
    ValidatePersonLastName,
    ValidateRoleCharacter,
    ValidateRoleImportance,
)


def domain_validators_provider_factory() -> Provider:
    provider = Provider(Scope.APP)

    provider.provide(ValidateMovieEngTitle)
    provider.provide(ValidateMovieOriginalTitle)
    provider.provide(ValidateMovieDuration)
    provider.provide(ValidateUserName)
    provider.provide(ValidatePersonFirstName)
    provider.provide(ValidatePersonLastName)
    provider.provide(ValidateRoleCharacter)
    provider.provide(ValidateRoleImportance)

    return provider
