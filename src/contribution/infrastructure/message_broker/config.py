from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class RabbitMQConfig:
    host: str
    port: int
    login: str
    password: Optional[str]
