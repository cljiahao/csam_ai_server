DENOISE_THRESHOLD: int = 50
THRESH_RANGE: dict[str, float] = {
    "low_chip_area": 0.15,
    "upp_chip_area": 2,
    "low_def_area": 0.75,
    "upp_def_area": 1.5,
}
BG_THRESHOLD: int = 130
COLOR_BACKGROUND: tuple[int, int, int] = (192, 192, 192)
COLOR_WHITE: tuple[int, int, int] = (255, 255, 255)
