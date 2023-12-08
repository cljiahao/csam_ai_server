import os
import cv2
import time

from apis.utils.batch_process import mask
from apis.utils.chip_process import chips
from apis.utils.image_process import create_border_img
from apis.utils.initialize import initialize


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


def inspect(image, lot_no, chip_type, db, get_ratio):
    """
    Parameters
    ----------
    image : numpy array
        Image to mask out background
    lot_no : str
        Lot number keyed in by user
    chip_type : str
        chip_type associated with lot number
    db : Session
        Database session
    get_ratio : Function
        function to get ratio based on web link

    Returns
    -------
    no_of_batches : int
        Number of batches found
    no_of_chips : int
        Number of chips found
    chips_dict: dict
        Key: batch, value: predicted NG's file name
    save_dir : str
        Directory of where the images are saved
    img_shape : list
        Image height and width
    """
    start = time.time()

    no_of_chips, no_of_batches, chips_dict, dir_dict = initialize(
        "CDC", image, lot_no, chip_type, db, get_ratio
    )

    new_start = time_print(start, "Directory Checking")

    border_img, gray, img_shape = create_border_img(image, dir_dict["save"])
    if any(chips_dict.values()):
        # If exists, return to quicken retrieval (caching)
        return (
            no_of_batches,
            no_of_chips,
            chips_dict,
            dir_dict["save"],
            img_shape,
        )

    batch_data = mask(gray, img_shape, chip_type)
    no_of_chips, temp_dict, ng_dict = chips(
        border_img, gray, batch_data, "CDC", chip_type
    )
    hold_dict = {**temp_dict, **ng_dict}

    new_start = time_print(new_start, "Chip Masking and Processing")

    no_of_batches = len(batch_data)
    chips_dict = {}
    for i in range(no_of_batches):
        chips_dict[f"Batch {i+1}"] = []

    for key, value in hold_dict.items():
        # Writing NG images into directory
        cv2.imwrite(os.path.join(dir_dict["temp"], key), value)
        if int(key.split("_")[1]) != 0:
            chips_dict["Batch " + key.split("_")[1]].append(key)
        elif "Stray" in chips_dict.keys():
            chips_dict["Stray"].append(key)
        else:
            chips_dict["Stray"] = []

    new_start = time_print(new_start, "Write and return individual chips")

    print(f"Total time taken: {round(time.time() - start,2)} secs")

    return no_of_batches, no_of_chips, chips_dict, dir_dict["save"], img_shape
