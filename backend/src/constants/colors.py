from dataclasses import dataclass


@dataclass
class BGRColors:
    BACKGROUND: tuple[int, int, int] = (192, 192, 192)
    BLACK: tuple[int, int, int] = (0, 0, 0)
    BLUE: tuple[int, int, int] = (255, 0, 0)
    CYAN: tuple[int, int, int] = (255, 255, 0)
    GREEN: tuple[int, int, int] = (0, 255, 0)
    LIME: tuple[int, int, int] = (255, 192, 0)
    ORANGE: tuple[int, int, int] = (0, 191, 255)
    RED: tuple[int, int, int] = (0, 0, 255)
    WHITE: tuple[int, int, int] = (255, 255, 255)
    YELLOW: tuple[int, int, int] = (0, 255, 255)


@dataclass
class HEXColors:
    WHITE: str = "#FFFFFF"
    YELLOW: str = "#FFFF00"
    CYAN: str = "#00FFFF"
