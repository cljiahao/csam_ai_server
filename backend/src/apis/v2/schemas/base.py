from enum import Enum

from db.models.CAI import CAI_DETAILS
from db.models.CDC import CDC_DETAILS


class Module(str, Enum):
    cai = "CAI"
    cdc = "CDC"


class CAIPage:
    model = CAI_DETAILS
    base_folder: str = "CAI"
    ai: bool = True


class CDCPage:
    model = CDC_DETAILS
    base_folder: str = "CDC"
    ai: bool = False
