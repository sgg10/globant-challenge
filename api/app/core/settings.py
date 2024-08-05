import os
from typing import Dict, List


class APISettings:
    PREFIX: str = ""
    API_NAME: str = os.environ.get("API_NAME", "Globant-Challaenge-API")
    VERSION: str = os.environ.get("VERSION", "v0.1.0")

    ORIGINS: List[str] = os.environ.get("ORIGINS", "*").split(",")

    ENVIRONMENT = os.environ.get("ENVIRONMENT", "local")

    # Database settings
    DATABASE: Dict[str, str | int] = {
        "HOST": os.environ.get("DB_HOST", "db"),
        "PORT": os.environ.get("DB_PORT", 5432),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
        "NAME": os.environ.get("DB_NAME", "mydb"),
    }
