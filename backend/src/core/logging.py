import json
import logging
import logging.config
import logging.handlers
from pathlib import Path
from datetime import datetime as dt

from core.config import common_settings
from core.directory import directory


class MyTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.namer = self.change_name

    def change_name(self, default_name: str) -> str:
        file_path = Path(default_name)
        tail = file_path.name

        mth_fol = directory.log_dir / dt.now().strftime("%b%Y")
        mth_fol.mkdir(parents=True, exist_ok=True)

        arr = tail.split(".")
        ext = arr.pop()
        fname = "_".join(arr) + f".{ext}"

        return str(mth_fol / fname)


logging.handlers.MyTimedRotatingFileHandler = MyTimedRotatingFileHandler


def setup_logging():
    logging_config_path = Path("./core/json/logging.json")

    if logging_config_path.exists():
        with logging_config_path.open("rt") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)


setup_logging()
logger = logging.getLogger(common_settings.ENV_STAGE)
