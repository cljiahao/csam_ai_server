import json


def read_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    return data


def write_json(file_path, dic):
    data = read_json(file_path)

    for k, v in dic.items():
        data[k] = v

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def read_txt(file_path):
    res = {}
    with open(file_path, "r") as f:
        data = f.readlines()
        for x in data:
            key, value = x.split("\n")[0].split(" ")
            res[key] = value

    return res


def write_txt(file_path, dic):
    txt_str = ""
    with open(file_path, "w") as f:
        for value in dic.values():
            txt_str += f"{value}|"
        f.write(txt_str[:-1])
