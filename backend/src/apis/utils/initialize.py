import os
from shutil import rmtree

from core.read_json import read_config
from apis.utils.cache import caching


def initialize(prog, image, lot_no, chip_type, db, get_ratio):
    """
    Parameters
    ----------
    image : numpy array
        Image to mask out background
    lot_no : str
        Lot number keyed in by user
    db : Session
        Database session

    Returns
    -------
    no_of_chips : int
        Number of chips
    no_of_batches : int
        Number of batches
    chips_dict : dict
        Chip filename saved in dictionary by batches
    dir_dict :
        Directory dictionary to save folder and files to
    """
    plate_no = image.filename.split(".")[0]
    dir_dict = check_dir(prog, chip_type, lot_no, plate_no)

    chips_dict = {}
    no_of_batches, no_of_chips = 0, 0
    if os.path.isdir(dir_dict["temp"]) and any(os.scandir(dir_dict["temp"])):
        try:
            # Pull data from database for caching
            ratio = get_ratio(lot_no=lot_no, plate_no=plate_no, db=db)
            no_of_batches = ratio.no_of_batches
            no_of_chips = ratio.no_of_chips
            for i in range(no_of_batches):
                chips_dict[f"Batch {i+1}"] = []
            caching(dir_dict, chips_dict)
        except:
            # If no data is found in database
            rm_and_make(dir_dict)
    else:
        rm_and_make(dir_dict)

    return no_of_batches, no_of_chips, chips_dict, dir_dict


def check_dir(prog, chip_type, lot_no, plate_no):
    dir_dict = {}
    fol_dict = read_config("./core/json/settings.json")

    backend_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    )
    chip_type_dir = os.path.join(backend_dir, "images", prog, chip_type)
    lot_dir = os.path.join(chip_type_dir, lot_no)
    dir_dict["save"] = os.path.join(lot_dir, plate_no)
    dir_dict["temp"] = os.path.join(dir_dict["save"], "temp")

    for fol_name in fol_dict["folders"]:
        dir_dict[fol_name] = os.path.join(dir_dict["save"], fol_name)
        if not os.path.exists(dir_dict[fol_name]):
            os.makedirs(dir_dict[fol_name])

    # Testing directory to be remove every testing
    if lot_no.lower()[:4] == "test" and os.path.isdir(lot_dir):
        rmtree(lot_dir)

    return dir_dict


def rm_and_make(dir_dict):
    if os.path.isdir(dir_dict["save"]):
        rmtree(dir_dict["save"])
    os.makedirs(dir_dict["temp"])
