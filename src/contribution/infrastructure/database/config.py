from dataclasses import dataclass
from urllib.parse import quote_plus

from contribution.infrastructure.get_env import get_env


@dataclass(frozen=True, slots=True)
class MongoDBConfig:
    username: str
    password: str
    host: str
    port: int

    @property
    def uri(self) -> str:
        return "mongodb://{username}:{password}@{host}".format(
            username=quote_plus(self.username),
            password=quote_plus(self.password),
            host=quote_plus(self.host),
        )


def mongodb_config_from_env() -> MongoDBConfig:
    return MongoDBConfig(
        username=get_env("MONGODB_USER"),
        password=get_env("MONGODB_PASSWORD"),
        host=get_env("MONGODB_HOST"),
        port=int(get_env("MONGODB_PORT")),
    )
