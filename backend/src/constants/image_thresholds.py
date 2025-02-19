from dataclasses import dataclass


@dataclass
class ImageThreshold:
    BATCH_MULTIPLIER: float = 0.01
    CHECK_SINGLE_THRESHOLD: int = 10
    DENOISE_THRESHOLD: int = 50
    BACKGROUND_THRESHOLD: int = 130
