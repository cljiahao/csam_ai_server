from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path=find_dotenv())


class Settings(BaseSettings):
    __config__ = ConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


class CommonSettings(Settings):
    PROJECT_NAME: str = "CSAM AI SERVER"
    PROJECT_VERSION: str = "v1.0.0"
    ENV_STAGE: str = "stage"


class APISettings(Settings):
    FASTAPI_ROOT: str = "/api"
    PC_NAME: str = "localhost"
    NGINX_PORT: int = 5173

    @property
    def ALLOWED_CORS(self) -> list[str]:
        # Compute ALLOWED_CORS based on the current values of PC_NAME and NGINX_PORT
        return [
            f"http://{self.PC_NAME}:{self.NGINX_PORT}",
            "http://localhost:5173",
        ]

    @field_validator("FASTAPI_ROOT", mode="before")
    def remove_trailing_slash(cls, value: str) -> str:
        # Remove any trailing slashes from the value
        return value.rstrip("/")


class DatabaseSettings(Settings):
    DB_NAME: str = "local.db"
    REALTIMEDB: str = ""
    TABLEID_CDC: str = ""
    TABLEID_CAI: str = ""


class ServiceSettings(Settings):
    TEST_LOT_NO: str = "1234567890"
    TEST_ITEM: str = "GCM32ER71E106KA59_+B55-E01GJ"
    PRASS_URL: str = ""
    LOT_COLUMN: str = ""
    ITEM_COLUMN: str = ""


common_settings = CommonSettings()
api_settings = APISettings()
service_settings = ServiceSettings()
database_settings = DatabaseSettings()
