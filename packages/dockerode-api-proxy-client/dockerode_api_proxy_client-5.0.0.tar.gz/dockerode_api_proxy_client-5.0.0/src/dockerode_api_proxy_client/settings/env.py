import os

from dataclasses import dataclass


@dataclass
class Environment:
    JWT_SECRET: str
    DOPPLER_TOKEN: str


def get_environment_enum():
    jwtSecret = os.getenv("JWT_SECRET")
    dopplerToken = os.getenv("DOPPLER_TOKEN")
    return Environment(jwtSecret, dopplerToken)
