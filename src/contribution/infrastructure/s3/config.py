from dataclasses import dataclass

from contribution.infrastructure.get_env import env_var_by_key


@dataclass(frozen=True, slots=True)
class MinIOConfig:
    url: str
    access_key: str
    secret_key: str
    bucket: str


def minio_config_from_env() -> MinIOConfig:
    return MinIOConfig(
        url=env_var_by_key("MINIO_URL"),
        access_key=env_var_by_key("MINIO_ACCESS_KEY"),
        secret_key=env_var_by_key("MINIO_SECRET_KEY"),
        bucket=env_var_by_key("MINIO_BUCKET"),
    )
