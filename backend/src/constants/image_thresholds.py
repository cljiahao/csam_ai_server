from enum import Enum


class ImageThreshold(Enum):
    BATCH_MULTIPLIER = 0.01
    CHECK_SINGLE_THRESHOLD = 10
    DENOISE_THRESHOLD = 50
    BACKGROUND_THRESHOLD = 130
