from dataclasses import dataclass


@dataclass
class ChipThresholdRatio:
    LOWER_CHIP_RATIO: float = 0.15
    UPPER_CHIP_RATIO: float = 2.0
    LOWER_DEFECT_RATIO: float = 0.75
    UPPER_DEFECT_RATIO: float = 1.5


@dataclass
class ChipThreshold:
    def __init__(self):
        self.ratio = ChipThresholdRatio
        self.LOWER_CHIP_AREA: float = 0.0
        self.UPPER_CHIP_AREA: float = 0.0
        self.LOWER_DEFECT_AREA: float = 0.0
        self.UPPER_DEFECT_AREA: float = 0.0

    def apply_ratios(self, average_area: float) -> None:
        """Calculate chip and defect area thresholds based on ratios and average area."""
        self.LOWER_CHIP_AREA = self.ratio.LOWER_CHIP_RATIO * average_area
        self.UPPER_CHIP_AREA = self.ratio.UPPER_CHIP_RATIO * average_area
        self.LOWER_DEFECT_AREA = self.ratio.LOWER_DEFECT_RATIO * average_area
        self.UPPER_DEFECT_AREA = self.ratio.UPPER_DEFECT_RATIO * average_area
