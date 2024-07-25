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


def time_print(func_name, lap=False, start=False) -> None:
    """
    Parameters
    ----------
    func_name : string
        Description for previous recording
    lap : float
        Lap time from previous recording
    start : float
        Start time from initial recording
    """
    if lap:
        if start:
            print(f"Last Process: {func_name}, took: {round(time.time()-lap,2)} secs")
            print(f"Total time taken: {round(time.time()-start,2)} secs")
        else:
            print(f"{func_name} took: {round(time.time()-lap,2)} secs")
    else:
        print(f"Start Process: {func_name}, please wait ...")

    return time.time()
