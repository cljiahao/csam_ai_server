import numpy as np

from utils.imageProcess.chip_process import get_chips
from utils.imageProcess.batch_process import get_batch


def test_get_batch(
    sample_images: dict[str, str | np.ndarray],
    sample_batch_config: dict[str, tuple[int, int]],
) -> None:
    """Test the retrieval of batch data from grayscale image."""

    result = get_batch(
        sample_images["gray"],
        sample_batch_config,
    )
    expected_result = 15

    assert len(result) == expected_result


def test_get_chips(
    sample_images: dict[str, str | np.ndarray],
    sample_batch_data: list[dict[str, float | int]],
    sample_chip_config: dict[str, tuple[int, int]],
) -> None:
    """Test the retrieval of chips from images."""

    expected_chip_count = int(sample_images["base_file_name"].split("_")[0])

    no_of_chips, temp_dict, ng_dict = get_chips(
        sample_images["border"],
        sample_images["gray"],
        sample_batch_data,
        sample_chip_config,
    )

    assert no_of_chips == expected_chip_count
    assert isinstance(temp_dict, dict)
    assert isinstance(ng_dict, dict)
    assert len(temp_dict.values()) + len(ng_dict.values()) == expected_chip_count
