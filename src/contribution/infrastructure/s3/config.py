from dataclasses import dataclass

from contribution.infrastructure.get_env import env_var_by_key


def s3_config_from_env() -> "S3Config":
    return S3Config(
        url=env_var_by_key("S3_URL"),
        access_key=env_var_by_key("S3_ACCESS_KEY"),
        secret_key=env_var_by_key("S3_SECRET_KEY"),
        bucket=env_var_by_key("S3_BUCKET"),
    )


@dataclass(frozen=True, slots=True)
class S3Config:
    url: str
    access_key: str
    secret_key: str
    bucket: str
