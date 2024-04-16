import os
from fastapi import HTTPException
import requests
from datetime import datetime as dt

from apis.utils.directory import dire
from core.config import settings


def write_csv(path, table_id, data, dic):
    for value in dic.values():
        data += f"{value},"
    file_name = (
        f"{table_id}_{dt.now().strftime('%d%m%y')}_{dt.now().strftime('%H%M%S')}.csv"
    )
    file_path = os.path.join(path, file_name)
    with open(file_path, "w") as f:
        f.write(data[:-1])

    return file_path


def via_http(file_path):
    # To Send via HTTP
    files = {"file": open(file_path, "rb")}
    resp = requests.post(settings.REALTIMEDB, files=files)

    print(
        f"File Size from server: {int(resp.content)}, Actual File Size: {os.stat(os.path.join(file_path)).st_size}"
    )

    if int(resp.content) != os.stat(os.path.join(file_path)).st_size:
        raise HTTPException(
            status_code=522,
            detail=f"File did not send to file server.",
        )
