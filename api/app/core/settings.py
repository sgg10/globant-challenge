import os
from typing import Dict, List

from app.core import constants


class APISettings:
    PREFIX: str = constants.API_PREFIX
    API_NAME: str = constants.API_NAME
    VERSION: str = constants.API_VERSION

    ORIGINS: List[str] = constants.API_ORIGINS.split(",")

    ENVIRONMENT = constants.API_ENVIRONMENT

    # Database settings
    DATABASE: Dict[str, str | int] = {
        "HOST": constants.DB_HOST,
        "PORT": constants.DB_PORT,
        "USER": constants.DB_USER,
        "PASSWORD": constants.DB_PASS,
        "NAME": constants.DB_NAME,
    }

    # Kafka settings
    KAFKA: Dict[str, str | int] = {
        "HOST": constants.KAFKA_HOST,
        "PORT": constants.KAFKA_PORT,
        "TOPIC": constants.KAFKA_TOPIC,
    }
