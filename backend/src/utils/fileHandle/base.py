import os
import json


def read_json(file_path: str) -> dict:

    if not os.path.exists(file_path):
        data = {}
        write_json(file_path, data)
    else:
        with open(file_path, "r") as f:
            data = json.load(f)

    return data


def write_json(file_path: str, data: dict) -> None:

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def read_txt(file_path: str) -> list:

    if not os.path.exists(file_path):
        write_txt()
        data = []
    with open(file_path, "r") as f:
        data = f.readlines()

    return data


def write_txt(file_path: str, data: str) -> None:

    with open(file_path, "w") as f:
        f.write(data)


# TODO: Write csv
def write_csv(file_path: str) -> None:

    return
