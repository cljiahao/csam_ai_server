from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path=find_dotenv())


class Settings(BaseSettings):
    """Base settings configuration."""

    __config__ = ConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


class CommonSettings(Settings):
    """Common settings for the application."""

    PROJECT_NAME: str = "CSAM AI SERVER"
    PROJECT_VERSION: str = "v2.0.0"
    ENV_STAGE: str = "stage"


class APISettings(Settings):
    """API-specific settings."""

    PC_NAME: str = "localhost"
    NGINX_PORT: int = 8080
    API_PORT: int = 8000

    @property
    def ALLOWED_CORS(self) -> list[str]:
        """Compute allowed CORS origins based on PC_NAME and NGINX_PORT."""
        return [
            f"http://{self.PC_NAME}:{self.NGINX_PORT}",
            "http://localhost:5173",
        ]


class DatabaseSettings(Settings):
    """Database configuration settings."""

    DB_NAME: str = "local.db"
    REALTIMEDB: str = ""
    TABLEID_CDC: str = ""
    TABLEID_CAI: str = ""


class ServiceSettings(Settings):
    """Service-specific settings."""

    TEST_LOT_NO: str = "1234567890"
    TEST_ITEM: str = "GCM32ER71E106KA59_+B55-E01GJ"
    PRASS_URL: str = ""
    LOT_COLUMN: str = ""
    ITEM_COLUMN: str = ""


# Instantiate settings
common_settings = CommonSettings()
api_settings = APISettings()
database_settings = DatabaseSettings()
service_settings = ServiceSettings()
