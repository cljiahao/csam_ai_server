# import math
# import os
# import cv2
# import numpy as np
# from pathlib import Path

# from utils.imageProcess.image_utils import (
#     chunking,
#     denoise_mask_image,
#     get_median_area,
# )
# from utils.imageProcess.chip_process import get_chips, mask_chips
# from utils.imageProcess.batch_process import get_batch
# from utils.imageProcess.image_process import create_border_image

# from db.models.CAI import CAI_DETAILS


# def cvWin(image: np.ndarray, name: str = "image"):
#     cv2.namedWindow(name, cv2.WINDOW_FREERATIO)
#     cv2.imshow(name, image)
#     cv2.waitKey(0)


# def get_border_and_gray(file_path: Path):

#     image = cv2.imread(str(file_path))
#     border_image, border_gray = create_border_image(image)

#     # cvWin(border_image)
#     # cvWin(border_gray)

#     file_name = file_path.name
#     cv2.imwrite(str(file_path.parent / f"border_{file_name}"), border_image)
#     cv2.imwrite(str(file_path.parent / f"gray_{file_name}"), border_gray)


# assets_path = Path(
#     r"C:\Users\MES21106\Desktop\CSAM Code\csam_ai_server\v2\backend\tests\assets"
# )

# settings = {
#     "batch": {"erode": (5, 5), "close": (37, 37)},
#     "chip": {"erode": (5, 5), "close": (2, 2)},
# }

# filtered_files = [
#     file for file in assets_path.glob("*.*") if len(file.name.split("_")) == 2
# ]

# batch_data = [
#     {"index": 200182.5, "x1": 139, "y1": 110, "x2": 226, "y2": 249},
#     {"index": 200360.5, "x1": 308, "y1": 110, "x2": 413, "y2": 245},
#     {"index": 200534.0, "x1": 479, "y1": 109, "x2": 589, "y2": 232},
#     {"index": 200717.0, "x1": 661, "y1": 112, "x2": 773, "y2": 251},
#     {"index": 200895.0, "x1": 835, "y1": 111, "x2": 955, "y2": 254},
#     {"index": 400167.0, "x1": 111, "y1": 310, "x2": 223, "y2": 453},
#     {"index": 400353.0, "x1": 296, "y1": 310, "x2": 410, "y2": 457},
#     {"index": 400533.0, "x1": 472, "y1": 309, "x2": 594, "y2": 448},
#     {"index": 400725.5, "x1": 680, "y1": 309, "x2": 771, "y2": 453},
#     {"index": 400895.0, "x1": 850, "y1": 309, "x2": 940, "y2": 435},
#     {"index": 600175.0, "x1": 113, "y1": 513, "x2": 237, "y2": 655},
#     {"index": 600355.5, "x1": 298, "y1": 509, "x2": 413, "y2": 650},
#     {"index": 600532.5, "x1": 470, "y1": 518, "x2": 595, "y2": 653},
#     {"index": 600720.5, "x1": 663, "y1": 510, "x2": 778, "y2": 634},
#     {"index": 600898.5, "x1": 847, "y1": 519, "x2": 950, "y2": 658},
# ]

# contours = [
#     ([], 232.5),
#     ([], 266.0),
#     ([], 237.5),
#     ([], 267.0),
#     ([], 260.0),
#     ([], 267.5),
#     ([], 293.5),
#     ([], 282.5),
#     ([], 249.0),
#     ([], 275.5),
#     ([], 280.0),
#     ([], 228.5),
#     ([], 260.0),
#     ([], 294.0),
#     ([], 300.0),
#     ([], 261.5),
#     ([], 254.0),
#     ([], 269.0),
#     ([], 260.0),
#     ([], 294.0),
#     ([], 254.0),
#     ([], 290.0),
#     ([], 253.5),
#     ([], 300.0),
#     ([], 263.5),
#     ([], 270.0),
#     ([], 257.5),
#     ([], 259.5),
#     ([], 260.5),
#     ([], 248.0),
#     ([], 271.5),
#     ([], 270.0),
#     ([], 303.0),
#     ([], 270.0),
#     ([], 255.5),
#     ([], 287.0),
#     ([], 277.0),
#     ([], 303.0),
#     ([], 280.5),
#     ([], 289.0),
#     ([], 301.0),
#     ([], 300.0),
#     ([], 291.5),
#     ([], 279.0),
#     ([], 280.0),
#     ([], 278.5),
#     ([], 286.5),
#     ([], 269.0),
#     ([], 271.0),
#     ([], 252.0),
# ]


# for file_path in filtered_files:

#     # get_border_and_gray(file_path)

#     file_name = file_path.name
#     border_image_path = file_path.parent / ("border_" + file_name)
#     border_gray_image_path = file_path.parent / ("gray_" + file_name)

#     border_image = cv2.imread(str(border_image_path))
#     border_gray_image = cv2.cvtColor(
#         cv2.imread(str(border_gray_image_path)), cv2.COLOR_BGR2GRAY
#     )

#     # batch_data = get_batch(border_gray_image, settings["batch"])

#     # mask_image = mask_chips(
#     #     border_gray_image, settings["chip"]["erode"], settings["chip"]["close"]
#     # )
#     # clean_contours = denoise_mask_image(mask_image)

#     # avg_chip_area = get_median_area(clean_contours)

#     # chunk_contours = chunking(clean_contours)

#     expected_chip_count = int(file_name.split("_")[0])

#     no_of_chips, temp_dict, ng_dict = get_chips(
#         border_image,
#         border_gray_image,
#         batch_data,
#         settings["chip"],
#     )
