import os
import json


def read_config(file_path):
    with open(file_path, "r") as f:
        config = json.load(f)

    return config


def write_config(file_path, dic):
    config = read_config(file_path)

    for k, v in dic.items():
        config[k] = v

    with open(file_path, "w") as f:
        json.dump(config, f, indent=4)
