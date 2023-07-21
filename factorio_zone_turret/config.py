from dataclasses import dataclass

from dotenv import dotenv_values


@dataclass
class Config:
    FZ_TOKEN: str
    FZ_SERVER_REGION: str
    FZ_SERVER_VERSION: str
    FZ_SERVER_SAVE: str


# load config from .env file
config = Config(**dotenv_values(".env"))
