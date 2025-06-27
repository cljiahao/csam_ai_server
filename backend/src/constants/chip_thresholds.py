from enum import Enum


class ChipThresholdRatio(Enum):
    LOWER_CHIP_RATIO = 0.15
    UPPER_CHIP_RATIO = 2.0
    LOWER_DEFECT_RATIO = 0.75
    UPPER_DEFECT_RATIO = 1.5


class ChipThreshold:
    def __init__(self):
        self.LOWER_CHIP_AREA: float = 0.0
        self.UPPER_CHIP_AREA: float = 0.0
        self.LOWER_DEFECT_AREA: float = 0.0
        self.UPPER_DEFECT_AREA: float = 0.0

    def apply_ratios(self, average_area: float) -> None:
        """Calculate chip and defect area thresholds based on ratios and average area."""
        self.LOWER_CHIP_AREA = ChipThresholdRatio.LOWER_CHIP_RATIO.value * average_area
        self.UPPER_CHIP_AREA = ChipThresholdRatio.UPPER_CHIP_RATIO.value * average_area
        self.LOWER_DEFECT_AREA = (
            ChipThresholdRatio.LOWER_DEFECT_RATIO.value * average_area
        )
        self.UPPER_DEFECT_AREA = (
            ChipThresholdRatio.UPPER_DEFECT_RATIO.value * average_area
        )
