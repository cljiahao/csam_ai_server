import os
from shutil import move, copyfile

from core.read_json import read_config


def caching(dir_dict, chips_dict):
    """
    Parameters
    ----------
    dir_dict : dict
        Directory dictionary to look for existing images to cache
    chips_dict : dict
        Chip dictionary to cache existing file names

    Returns
    -------
    None
    """
    dir_dict.pop("save")
    for key, dir_path in dir_dict.items():
        if key == "temp":
            chips_dict = img_cache(dir_path, chips_dict)
        elif os.path.isdir(dir_path) and any(os.scandir(dir_path)):
            chips_dict = img_cache(dir_path, chips_dict)


def img_cache(directory, chips):
    """
    Parameters
    ----------
    directory : str
        Directory to check if files exists
    chips : dict
        Chip filename saved in dictionary by batches

    Returns
    -------
    chips : dict
        Chip filename saved in dictionary by batches
    """
    for file in os.listdir(directory):
        if file.split(".")[-1] == "png":
            if int(file.split("_")[1]) != 0:
                chips[f"Batch {file.split('_')[1]}"].append(file)
            elif "Stray" in chips.keys():
                chips["Stray"].append(file)
            else:
                chips["Stray"] = []

    return chips


def selected(directory, real_ng_dict):
    """
    Parameters
    ----------
    directory : str
        Directory to compare selected and existing files
    real_ng_dict : dict
        Defect chips selected

    Returns
    -------
    None
    """

    # Define file_modes based on user settings (Folder names)
    file_mode = {"temp": "0"}
    fol_dict = read_config("./core/json/settings.json")
    for i, j in enumerate(fol_dict["folders"]):
        file_mode[j] = str(i + 1)

    # Define current location of saved files
    holder = {}
    folders = os.listdir(directory)
    folders.remove("original")
    for fol in folders:
        for os_file in os.listdir(os.path.join(directory, fol)):
            holder[os_file[1:]] = [fol, os_file]

    # Movement of files to new location based on user input
    for next_fol in real_ng_dict:
        dest = os.path.join(directory, next_fol)
        if not os.path.isdir(dest):
            os.makedirs(dest)

        for id, old_fname in real_ng_dict[next_fol].items():
            file_name = old_fname[1:]
            new_fname = file_mode[next_fol] + file_name
            prev_fol_file = holder[file_name]
            src = os.path.join(directory, prev_fol_file[0])

            move(
                os.path.join(src, prev_fol_file[1]),
                os.path.join(dest, new_fname),
                copy_function=copyfile,
            )

            holder.pop(file_name)

    for fol, fname in holder.values():
        if fol == "temp":
            continue
        move(
            os.path.join(directory, fol, fname),
            os.path.join(directory, "temp", "0" + fname[1:]),
            copy_function=copyfile,
        )
