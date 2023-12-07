import os
from datetime import datetime as dt

from core.config import settings


def create_csv(ratio, directory):
    data = ",,,"
    for k in range(len(ratio)):
        data += f"{ratio[k]},"
    file_name = f"{settings.TABLEID}_{dt.now().strftime('%d%m%y')}_{dt.now().strftime('%H%M%S')}.csv"
    file_path = os.path.join(directory, file_name)
    with open(file_path, "w") as f:
        f.write(data[:-1])

    return file_path
