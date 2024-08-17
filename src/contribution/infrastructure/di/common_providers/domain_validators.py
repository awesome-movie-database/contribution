from dishka import Provider, Scope

from contribution.domain import (
    ValidateMovieEngTitle,
    ValidateMovieOriginalTitle,
    ValidateMovieSummary,
    ValidateMovieDescription,
    ValidateMovieDuration,
    ValidateUserName,
    ValidateEmail,
    ValidateTelegram,
    ValidatePersonFirstName,
    ValidatePersonLastName,
    ValidateRoleCharacter,
    ValidateRoleImportance,
)


def domain_validators_provider_factory() -> Provider:
    provider = Provider(Scope.APP)

    provider.provide(ValidateMovieEngTitle)
    provider.provide(ValidateMovieOriginalTitle)
    provider.provide(ValidateMovieSummary)
    provider.provide(ValidateMovieDescription)
    provider.provide(ValidateMovieDuration)
    provider.provide(ValidateUserName)
    provider.provide(ValidateEmail)
    provider.provide(ValidateTelegram)
    provider.provide(ValidatePersonFirstName)
    provider.provide(ValidatePersonLastName)
    provider.provide(ValidateRoleCharacter)
    provider.provide(ValidateRoleImportance)

    return provider
