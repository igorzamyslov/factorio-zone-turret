from dataclasses import dataclass

from dotenv import dotenv_values


@dataclass
class Config:
    FZ_TOKEN: str


# load config from .env file
config = Config(**dotenv_values(".env"))
