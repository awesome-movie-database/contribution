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

    provider.provide(ValidateMovieEngTitle, provides=ValidateMovieEngTitle)
    provider.provide(
        ValidateMovieOriginalTitle,
        provides=ValidateMovieOriginalTitle,
    )
    provider.provide(ValidateMovieDuration, provides=ValidateMovieDuration)
    provider.provide(ValidateUserName, provides=ValidateUserName)
    provider.provide(ValidatePersonFirstName, provides=ValidatePersonFirstName)
    provider.provide(ValidatePersonLastName, provides=ValidatePersonLastName)
    provider.provide(ValidateRoleCharacter, provides=ValidateRoleCharacter)
    provider.provide(ValidateRoleImportance, provides=ValidateRoleImportance)

    return provider
