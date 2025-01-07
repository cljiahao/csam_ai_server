from enum import Enum


class Module(str, Enum):
    cai = "CAI"
    cdc = "CDC"


class CAIPage:
    base_folder: str = "CAI"
    ai: bool = True


class CDCPage:
    base_folder: str = "CDC"
    ai: bool = False
