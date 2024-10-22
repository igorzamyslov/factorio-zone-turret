from dataclasses import dataclass

from dotenv import dotenv_values


@dataclass
class Config:
    FZ_TOKEN: str
    FZ_SERVER_REGION: str
    FZ_SERVER_VERSION: str
    FZ_SERVER_SAVE: str
    FZ_SERVER_IPV6: bool


# load config from .env file
env_vars = dotenv_values(".env")
env_vars["FZ_SERVER_IPV6"] = (env_vars["FZ_SERVER_IPV6"] == "True")
config = Config(**env_vars)
