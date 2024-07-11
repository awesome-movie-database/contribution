from uuid_extensions import uuid7

from contribution.application import OperationId


def default_operation_id_factory() -> OperationId:
    """
    Factory of OperationId that should be used if
    interactor call initializer is admin
    (for example if interactor was called from cli)
    or no other operation was provided.
    """
    return OperationId(uuid7().hex)
