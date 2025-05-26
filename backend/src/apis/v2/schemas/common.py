from dataclasses import dataclass
from enum import StrEnum

from apis.v2.constants.csam_thresholds import ChipThresholdRatio


class ServerMode(StrEnum):
    CAI = "CAI"
    CDC = "CDC"


@dataclass
class ChipThreshold:
    """Class to manage chip and defect area thresholds."""

    def __init__(self) -> None:
        """Initializes the chip and defect area thresholds."""
        self.LOWER_CHIP_AREA: float = 0.0
        self.UPPER_CHIP_AREA: float = 0.0
        self.LOWER_DEFECT_AREA: float = 0.0
        self.UPPER_DEFECT_AREA: float = 0.0

    def apply_ratios(self, average_area: float) -> None:
        """Calculate chip and defect area thresholds based on ratios and average area."""
        self.LOWER_CHIP_AREA = (
            ChipThresholdRatio.LOWER_CHIP_AREA_RATIO.value * average_area
        )
        self.UPPER_CHIP_AREA = (
            ChipThresholdRatio.UPPER_CHIP_AREA_RATIO.value * average_area
        )
        self.LOWER_DEFECT_AREA = (
            ChipThresholdRatio.LOWER_DEFECT_AREA_RATIO.value * average_area
        )
        self.UPPER_DEFECT_AREA = (
            ChipThresholdRatio.UPPER_DEFECT_AREA_RATIO.value * average_area
        )
