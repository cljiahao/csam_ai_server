import cv2
import time
import numpy as np
from datetime import timedelta

from core.exceptions import CustomErrorMessage
from core.logging import logger


def cvWin(image: np.ndarray, name: str = "image") -> None:
    """Display an image using OpenCV for debugging purposes.

    Args:
        image : np.ndarray
            The image to be displayed.
        name : str
            The name of the window. Defaults to "image".
    """

    cv2.namedWindow(name, cv2.WINDOW_FREERATIO)
    cv2.imshow(name, image)
    if cv2.waitKey(0) & 0xFF == ord("q"):
        cv2.destroyAllWindows()


def timer(print_message: str = ""):
    """A decorator to log the time taken by a function.

    Args:
        print_message : str
            A custom message to be logged along with the elapsed time.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = timedelta(seconds=end_time - start_time)
            formatted_time = str(elapsed_time).split(".")[0]
            if print_message:
                logger.info(f"{print_message} took: {formatted_time}", stacklevel=2)
            else:
                logger.info(f"Total time taken: {formatted_time}", stacklevel=2)
            return result

        return wrapper

    return decorator


def error_handler(
    print_message: str = "",
    custom_error: Exception = None,
):
    """A decorator to log exceptions that occur during the execution of a function.

    Args:
        print_message (str, optional): A custom message to be logged along with the exception details.
        custom_error (Exception, optional): A custom exception class to raise instead of the default exception.

    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except CustomErrorMessage as e:
                if custom_error:
                    raise custom_error(str(e))
                raise Exception(str(e))
            except Exception as e:
                if custom_error:
                    raise custom_error(print_message if print_message else str(e))
                raise e

        return wrapper

    return decorator
