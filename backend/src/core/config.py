import os
import json
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "CSAM AI SERVER"
    PROJECT_VERSION: str = "1.0.0"

    DBTYPE: str = os.getenv("DBTYPE")
    USER: str = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    SERVER: str = os.getenv("SERVER", "localhost")
    PORT: str = os.getenv("PORT", 5432)  # default postgres port is 5432
    DB: str = os.getenv("DB", "tdd")
    DATABASE_URL = f"{DBTYPE}://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DB}"

    CORS: list = json.loads(os.getenv("CORS"))
    PRASS_URL: str = os.getenv("PRASS_URL")
    LOT_COL: str = os.getenv("LOT_COL")
    ITEM_COL: str = os.getenv("ITEM_COL")
    ITEM: str = os.getenv("ITEM")

    REALTIMEDB: str = os.getenv("REALTIMEDB")
    TABLEID: str = os.getenv("TABLEID")

    G_TYPES: list = ["G", "Good", "g", "good"]

    CHIP_IMG_SIZE: list = [54, 54]


settings = Settings()
