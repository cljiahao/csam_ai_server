# Constants and default settings for image processing and configurations.

# Valid types for "G"
G_TYPES: list[str] = ["G", "Good", "g", "good"]

# Filenames for settings and color groups
SETTINGS_FILENAME: str = "settings.json"
COLOR_GROUP_FILENAME: str = "colors.json"

# Types and modes of settings
SETTINGS_TYPE: list[str] = ["batch", "chip"]
SETTINGS_MODE: list[str] = ["erode", "close"]

# Default settings for batch and chip processing
DEFAULT_SETTINGS: dict[str, dict[str, list[int]]] = {
    "batch": {"erode": [1, 1], "close": [1, 1]},
    "chip": {"erode": [1, 1], "close": [1, 1], "crop": [54, 54]},
}

# Default colors for various categories
DEFAULT_COLORS: dict[str, str] = {
    "NG": "#ffff00",  # Yellow for "Not Good"
    "Others": "#00ffff",  # Cyan for others
}
