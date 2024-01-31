import cv2
import time


def cvWin(img):
    """
    Parameters
    ----------
    img : numpy array
        Image to mask out background
    """
    cv2.namedWindow("img", cv2.WINDOW_FREERATIO)
    cv2.imshow("img", img)
    cv2.waitKey(0)


def time_print(start, func_name) -> None:
    """
    Parameters
    ----------
    start : float
        Start time from previous recording
    func_name : string
        Description for previous recording
    """
    print(f"{func_name} took: {round(time.time()-start,2)} secs")

    return time.time()
