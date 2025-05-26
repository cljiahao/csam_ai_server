from enum import StrEnum


class CSAMImageFolderName(StrEnum):
    ORIGINAL = "original"
    TEMP = "temp"


class BaseSetsFolderName(StrEnum):
    BASE = "base"
    NG = "ng"
    GOOD = "good"
    OTHERS = "others"
    DEFORM = "deform"
