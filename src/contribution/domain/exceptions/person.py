from .base import DomainError


class InvalidPersonFirstNameError(DomainError):
    ...


class InvalidPersonLastNameError(DomainError):
    ...


class InvalidPersonBirthOrDeathDateError(DomainError):
    ...
