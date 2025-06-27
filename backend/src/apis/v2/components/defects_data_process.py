import numpy as np
from itertools import chain
from functools import partial
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor

from apis.v2.helpers.processor.defect_processor import DefectProcessor
from schemas.chips_data import BatchDefectData, DefectData, ImageData
from schemas.contours import ContourInfo, ContourList
from utils.debug import timer
from utils.image_process.contour_handler import ContourHandler


@timer("Chunk contour processing")
def process_chunk_contours(
    defect_processor: DefectProcessor,
    base_file_name: str,
    refined_contours_info_list: ContourList,
    image: np.ndarray,
    border_pad: int,
) -> tuple[dict[str, list[DefectData]], list[ImageData], list[ImageData]]:
    """Process chunks of contours by splitting them and using multiprocessing."""
    chunked_contours = ContourHandler.chunking(refined_contours_info_list.contours)

    chunk_increment = len(chunked_contours[0])
    process_defects_partial = partial(
        chunk_process_defects,
        defect_processor=defect_processor,
        base_file_name=base_file_name,
        image=image,
        border_pad=border_pad,
        chunk_increment=chunk_increment,
    )

    with ProcessPoolExecutor() as exe:
        results = list(
            chain.from_iterable(
                exe.map(
                    process_defects_partial,
                    chunked_contours,
                    range(len(chunked_contours)),
                )
            )
        )

    return process_results(results)


def chunk_process_defects(
    chunk: ContourInfo,
    index: int,
    defect_processor: DefectProcessor,
    base_file_name: str,
    image: np.ndarray,
    border_pad: int,
    chunk_increment: int,
) -> list[tuple[BatchDefectData, ImageData]]:
    """Process a chunk of contours using the defect processor."""
    start_index = index * chunk_increment
    return [
        defect_processor.process_defects(
            f"{base_file_name}_{start_index+i}.png",
            image,
            contour_info,
            border_pad,
        )
        for i, contour_info in enumerate(chunk)
    ]


def process_results(
    results: list[tuple[BatchDefectData, ImageData]]
) -> tuple[dict[str, list[DefectData]], list[ImageData], list[ImageData]]:

    defect_batch_dict = defaultdict(list)
    image_predictions = {True: [], False: []}

    for batch_defect_data, image_data in results:
        defect_batch_dict[batch_defect_data.batch_no].append(
            batch_defect_data.defect_data
        )
        image_predictions[image_data.to_predict].append(image_data)

    return defect_batch_dict, image_predictions[True], image_predictions[False]
