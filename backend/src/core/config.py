from pydantic import field_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path=find_dotenv())


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


class CommonSettings(BaseSettings):
    PROJECT_NAME: str = "CSAM AI SERVER"
    PROJECT_VERSION: str = "v1.0.0"
    ENV_STAGE: str = "stage"


class APISettings(BaseSettings):
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


class DatabaseSettings(BaseSettings):
    LOCAL_DB_PATH: str = ""
    REALTIMEDB: str = ""
    TABLEID_CDC: str = ""
    TABLEID_CAI: str = ""


class ServiceSettings(Settings):
    TEST_ITEM: str = ""
    PRASS_URL: str = ""
    LOT_COLUMN: str = ""
    ITEM_COLUMN: str = ""


common_settings = CommonSettings()
api_settings = APISettings()
service_settings = ServiceSettings()
database_settings = DatabaseSettings()
