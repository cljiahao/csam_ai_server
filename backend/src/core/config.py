import os
import json

from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path=find_dotenv())


class Settings:
    PROJECT_NAME: str = "CSAM AI SERVER"
    PROJECT_VERSION: str = "2.0.0"

    FASTAPI_ROOT: str = f"{os.getenv('FASTAPI_ROOT')}"
    CORS: list = [f"http://{os.getenv('PC_NAME')}:{os.getenv('NGINX_PORT')}"]

    PRASS_URL: str = os.getenv("PRASS_URL")
    LOT_COL: str = os.getenv("LOT_COL")
    ITEM_COL: str = os.getenv("ITEM_COL")
    TEST_ITEM: str = os.getenv("TEST_ITEM")

    LOCAL_DB_PATH: str = os.getenv("LOCAL_DB_PATH")

    REALTIMEDB: str = os.getenv("REALTIMEDB")
    TABLEID_CDC: str = os.getenv("TABLEID_CDC")
    TABLEID_CAI: str = os.getenv("TABLEID_CAI")

    G_TYPES: list = ["G", "Good", "g", "good"]

    CHIP_IMG_SIZE: list = [54, 54]


settings = Settings()
