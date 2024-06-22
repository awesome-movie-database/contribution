from dataclasses import dataclass

from contribution.infrastructure.get_env import env_var_by_key


@dataclass(frozen=True, slots=True)
class RedisConfig:
    url: str


def redis_config_from_env() -> RedisConfig:
    return RedisConfig(
        url=env_var_by_key("REDIS_URL"),
    )
