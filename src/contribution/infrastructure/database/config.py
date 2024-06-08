from dataclasses import dataclass
from urllib.parse import quote_plus

from contribution.infrastructure.get_env import env_var_by_key


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
        username=env_var_by_key("MONGODB_USER"),
        password=env_var_by_key("MONGODB_PASSWORD"),
        host=env_var_by_key("MONGODB_HOST"),
        port=int(env_var_by_key("MONGODB_PORT")),
    )
