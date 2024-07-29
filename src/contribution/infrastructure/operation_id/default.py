from uuid_extensions import uuid7

from contribution.application import OperationId


def default_operation_id_factory() -> OperationId:
    """
    Factory of OperationId that should be used if
    initializer of interactor call is admin
    (for example if interactor was called from cli)
    or no other operation id was provided.
    """
    return OperationId(uuid7().hex)
