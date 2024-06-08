import os
from dataclasses import dataclass
from typing import Optional

from contribution.infrastructure.get_env import env_var_by_key


@dataclass(frozen=True, slots=True)
class RabbitMQConfig:
    host: str
    port: int
    login: str
    password: Optional[str]


def rabbitmq_config_from_env() -> RabbitMQConfig:
    return RabbitMQConfig(
        host=env_var_by_key("RABBITMQ_HOST"),
        port=int(env_var_by_key("RABBITMQ_PORT")),
        login=env_var_by_key("RABBITMQ_LOGIN"),
        password=os.getenv("RABBITMQ_PASSWORD"),
    )
