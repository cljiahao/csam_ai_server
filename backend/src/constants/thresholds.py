from dataclasses import dataclass


@dataclass
class ImageThreshold:
    BATCH_MULTIPLIER: float = 0.01
    CHECK_SINGLE_THRESHOLD: int = 10
    DENOISE_THRESHOLD: int = 50
    BACKGROUND_THRESHOLD: int = 130


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
        self.lower_chip_area: float = 0.0
        self.upper_chip_area: float = 0.0
        self.lower_defect_area: float = 0.0
        self.upper_defect_area: float = 0.0

    def apply_ratios(self, average_area: float) -> None:
        """Calculate chip and defect area thresholds based on ratios and average area."""
        self.lower_chip_area = self.ratio.LOWER_CHIP_RATIO * average_area
        self.upper_chip_area = self.ratio.UPPER_CHIP_RATIO * average_area
        self.lower_defect_area = self.ratio.LOWER_DEFECT_RATIO * average_area
        self.upper_defect_area = self.ratio.UPPER_DEFECT_RATIO * average_area
