from pathlib import Path
from shutil import copyfile, move

# from concurrent.futures import ThreadPoolExecutor

from core.directory import directory
from utils.fileHandle.json import get_colors_json
from utils.osHandle.write_image import update_chip_dict


def get_cache_data(no_of_batches: int, plate_path: Path) -> dict[str, list[str]]:
    """Fetches cache data by scanning plate directories and organizing files into a dictionary."""

    chip_dict = {str(i + 1): [] for i in range(no_of_batches)}

    # Get all folder_paths in plate_path except the 'original' folder
    folders = [
        folder
        for folder in plate_path.iterdir()
        if folder.is_dir() and folder.name != "original"
    ]

    for folder in folders:
        for file_name in folder.iterdir():
            update_chip_dict(chip_dict, file_name.name)

    # TODO: Performance check if threading is required
    # with ThreadPoolExecutor() as executor:
    #     futures = []

    #     for folder in folders:
    #         for file_name in folder.iterdir():
    #             # Submit the update_chip_dict task and collect the future
    #             future = executor.submit(update_chip_dict, chip_dict, file_name.name)
    #             futures.append(future)  # Accumulate the futures

    #     # Ensure that all threads complete
    #     for future in futures:
    #         future.result()  # Wait for all futures to complete

    return chip_dict


def set_cache_data(item: str, relative_plate_path: str, selected: dict) -> bool:
    """Sets cache data by moving files into designated directories based on selection and configuration."""

    plate_path = directory.images_dir / relative_plate_path
    # Get all folders in plate_path except the 'original' folder
    folders = [
        folder
        for folder in plate_path.iterdir()
        if folder.is_dir() and folder.name != "original"
    ]

    holder = {}
    # Populate the holder dictionary with file information
    for folder in folders:
        for os_file in folder.iterdir():
            holder[os_file.name[1:]] = {
                "folder_name": folder.name,
                "file_path": os_file,
            }

    # Fetch color information from a JSON file
    colors_data = get_colors_json(item)

    # Process each selected item
    for key, value in selected.items():
        dest = plate_path / key
        dest.mkdir(parents=True, exist_ok=True)

        for fname in value:
            _fname = fname[1:]
            mode = next(
                (
                    index + 1
                    for index, color in enumerate(colors_data)
                    if color["category"] == key
                ),
                0,
            )
            new_fname = f"{mode}{_fname}"

            # Move the file to the new destination
            move(holder[_fname]["file_path"], dest / new_fname, copy_function=copyfile)
            holder.pop(_fname)

    # Move remaining files to the 'temp' folder if not already in 'temp
    for k, v in holder.items():
        if v["folder_name"] == "temp":
            continue
        move(
            v["file_path"],
            plate_path / "temp" / f"0{k}",
            copy_function=copyfile,
        )

    return True
