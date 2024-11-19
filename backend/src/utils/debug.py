import cv2
import time
import numpy as np
from typing import Optional


def cvWin(image: np.ndarray, name: str = "image") -> None:
    """Display an image using OpenCV for debugging purposes.

    Args:
        image (np.ndarray): The image to be displayed.
        name (str): The name of the window. Defaults to "image".
    """

    cv2.namedWindow(name, cv2.WINDOW_FREERATIO)
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def time_print(
    func_name: Optional[str] = None, lap: Optional[float] = None, end: bool = False
) -> tuple[float, str]:
    """Log the time taken for a function or process.

    Args:
        func_name (Optional[str]): The name of the function or process being timed. Defaults to None.
        lap (Optional[float]): The start time of the process. Defaults to None.
        end (bool): Flag to indicate if the timing should be marked as ended. Defaults to False.

    Returns:
        Tuple[float, str]: The current time and a message about the time taken.
    """

    current_time = time.time()
    if lap is not None:
        time_taken = round(current_time - lap, 2)
        stdout = (
            f"Total time taken: {time_taken} secs"
            if end
            else f"{func_name} took: {time_taken} secs"
        )
    else:
        stdout = f"Start Process: {func_name}, please wait ..."

    return current_time, stdout
