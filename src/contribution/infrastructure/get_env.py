import os


def env_var_by_key(key: str) -> str:
    """
    Returns value from env vars by key
    if value exists, otherwise raises
    Exception.
    """
    value = os.getenv(key)
    if not value:
        message = f"Env var {key} doesn't exist"
        raise Exception(message)
    return value
