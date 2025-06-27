from enum import Enum, IntEnum, StrEnum


class SettingsMode(StrEnum):
    CHIP = "chip"
    BATCH = "batch"


class ChipThresholdRatio(float, Enum):
    """Float Enum for chip and defect area ratios."""

    LOWER_CHIP_AREA_RATIO = 0.15
    UPPER_CHIP_AREA_RATIO = 2.0
    LOWER_DEFECT_AREA_RATIO = 0.75
    UPPER_DEFECT_AREA_RATIO = 1.5


class CSAMThresholdRatio(IntEnum):
    BACKGROUND_THRESHOLD = 130
    BRIGHT_BACKGROUND_THRESHOLD = 250
    DENOISE_THRESHOLD = 50


class AugmentThresholdRatio(IntEnum):
    BASE_MULTIPLIER = 10


class DefectSizeThreshold(IntEnum):
    SMALL = 5
    MEDIUM = 40


class DefectSizeType(StrEnum):
    SMALL = "small"
    MEDIUM = "medium"
    BIG = "big"
