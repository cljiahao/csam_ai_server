from enum import Enum, StrEnum


class ServerMode(StrEnum):
    CAI = "CAI"
    CDC = "CDC"


class CAIPage(Enum):
    base_folder = "CAI"
    is_ai = True


class CDCPage(Enum):
    base_folder = "CDC"
    is_ai = False
