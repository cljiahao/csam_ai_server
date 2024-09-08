CHIP_CROP_SIZE: list[int] = [54, 54]
G_TYPES: list[str] = ["G", "Good", "g", "good"]
SETTINGS_FILENAME: str = "settings.json"
COLOR_GROUP_FILENAME: str = "colors.json"
SETTINGS_TYPE = ["batch", "chip"]
SETTINGS_MODE = ["erode", "close"]
DEFAULT_SETTINGS = {
    "batch": {"erode": [1, 1], "close": [1, 1]},
    "chip": {"erode": [1, 1], "close": [1, 1]},
}
# TODO: add correct colors
DEFAULT_COLORS = {"NG": "#", "Others": "#"}
