from dataclasses import dataclass

from contribution.infrastructure.get_env import env_var_by_key


@dataclass(frozen=True, slots=True)
class RabbitMQConfig:
    url: str


def rabbitmq_config_from_env() -> RabbitMQConfig:
    return RabbitMQConfig(
        url=env_var_by_key("RABBITMQ_URL"),
    )
