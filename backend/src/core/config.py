import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path=find_dotenv())


class Settings:
    PROJECT_NAME: str = "CSAM AI SERVER"
    PROJECT_VERSION: str = "2.0.0"
    ENV_STAGE: str = os.getenv("ENV_STAGE", "stage")

    FASTAPI_ROOT: str = f"{os.getenv('FASTAPI_ROOT')}"
    # Uncomment to used with docker and nginx
    # FASTAPI_ROOT: str = f"{os.getenv('FASTAPI_ROOT')}/"
    CORS: list = [
        f"http://{os.getenv('PC_NAME')}:{os.getenv('NGINX_PORT')}",
        "http://localhost:5173",
    ]

    TEST_ITEM: str = os.getenv("TEST_ITEM")
    PRASS_URL: str = os.getenv("PRASS_URL")
    LOT_COL: str = os.getenv("LOT_COL")
    ITEM_COL: str = os.getenv("ITEM_COL")

    LOCAL_DB_PATH: str = os.getenv("LOCAL_DB_PATH")

    REALTIMEDB: str = os.getenv("REALTIMEDB")
    TABLEID_CDC: str = os.getenv("TABLEID_CDC")
    TABLEID_CAI: str = os.getenv("TABLEID_CAI")

    G_TYPES: list = ["G", "Good", "g", "good"]
    CHIP_IMG_SIZE: list = [54, 54]

    THRES_RANGE: dict = {
        "low_chip_area": 0.15,
        "upp_chip_area": 3,
        "low_def_area": 0.75,
        "upp_def_area": 1.5,
    }

    SETTINGS_FNAME: str = "settings.json"
    MODEL_EXT: list = [".h5", ".txt"]


settings = Settings()
