from schemas.misc import NormalizeCoordinates
from utils.debug import error_handler


@error_handler()
def normalize_coordinates(
    coordinates: list[int, int], image_size: list[int, int], padding: int = 0
) -> NormalizeCoordinates:
    """Normalizes a set of coordinates to the range [0, 1].

    Args:
        coordinates: A list or tuple containing the x and y coordinates [x, y].
        image_size: A list or tuple containing the height and width of the image [height, width].
        padding: An optional integer representing the border padding (default: 0).

    Returns:
        A NormalizeCoordinates object containing the normalized x and y values.
    """
    x, y = coordinates
    height, width = image_size

    norm_x = round((x - padding) / (width - padding * 2), 6)
    norm_y = round((y - padding) / (height - padding * 2), 6)

    return NormalizeCoordinates(norm_x=norm_x, norm_y=norm_y)


@error_handler()
def calculate_border_padding(crop_size: int) -> int:
    """Calculates the padding size for the border based on the crop size.

    Args:
        crop_size: The size of the cropped image (assuming square).

    Returns:
        The calculated border padding size, rounded to the nearest 10.
    """
    return ((crop_size * 141) // 100 + 9) // 10 * 10
