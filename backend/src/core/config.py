from pydantic import ConfigDict, Field, field_validator
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

    PROJECT_NAME: str = Field(default="My Project")
    PROJECT_VERSION: str = Field(default="v1.0.0")
    ENV_STAGE: str = Field(default="stage")


class APISettings(Settings):
    """API-specific settings."""

    FASTAPI_ROOT: str = Field(default="/api")
    PC_NAME: str = Field(default="locahost")
    NGINX_PORT: int = Field(default=8080)
    API_PORT: int = Field(default=8000)
    APP_PORT: int = Field(default=3000)
    DEV_API_PORT: int = Field(default=5000)
    DEV_APP_PORT: int = Field(default=5173)
    ALLOWED_CORS: list[str] = []

    def __init__(self, **data):
        super().__init__(**data)
        self.ALLOWED_CORS = self._compute_allowed_cors()

    def _compute_allowed_cors(self) -> list[str]:
        """Compute allowed CORS origins based on PC_NAME and NGINX_PORT."""
        cors = ["http://localhost:5173", f"http://{self.PC_NAME}:{self.NGINX_PORT}"]
        if common_settings.ENV_STAGE == "stage":
            cors.append(f"http://{self.PC_NAME}:{self.APP_PORT}")
        else:
            cors.append(f"http://{self.PC_NAME}:{self.DEV_APP_PORT}")
        return cors

    @field_validator("FASTAPI_ROOT", mode="before")
    def remove_trailing_slash(cls, value: str) -> str:
        """Remove any trailing slashes from FASTAPI_ROOT."""
        return value.rstrip("/")


class DatabaseSettings(Settings):
    """Database configuration settings."""

    DB_NAME: str = Field(default="local.db")
    REALTIMEDB: str = Field(default="")
    TABLEID_CDC: str = Field(default="")
    TABLEID_CAI: str = Field(default="")


class ServiceSettings(Settings):
    """Service-specific settings."""

    TEST_LOT_NO: str = Field(default="1234567890")
    TEST_ITEM: str = Field(default="GCM32ER71E106KA59_+B55-E01GJ")
    PRASS_URL: str = Field(default="")
    LOT_COLUMN: str = Field(default="")
    ITEM_COLUMN: str = Field(default="")


# Instantiate settings
common_settings = CommonSettings()
api_settings = APISettings()
database_settings = DatabaseSettings()
service_settings = ServiceSettings()
