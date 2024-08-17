import os


class Directory:
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    # Log folder
    log_dir = os.path.join(base_dir, "log")

    # Config folder
    config_dir = os.path.join(base_dir, "config")
    json_dir = os.path.join(config_dir, "json")
    model_dir = os.path.join(config_dir, "model")

    # Data folder
    data_dir = os.path.join(base_dir, "data")
    images_dir = os.path.join(data_dir, "images")
    data_send_dir = os.path.join(data_dir, "datasend")


directory = Directory()
