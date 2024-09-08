import cv2
import pytest
import numpy as np
from pathlib import Path

# Define the path to the assets directory
current_path = Path(__file__)
assets_path = current_path.parent.parent.parent / "assets"


def filtered_files() -> list[Path]:
    """Return a list of base test file paths."""
    return [file for file in assets_path.glob("*.*") if len(file.name.split("_")) == 2]


@pytest.fixture(params=filtered_files())
def sample_images(request: pytest.FixtureRequest) -> dict[str, str | np.ndarray]:
    """Fixture to load sample images for testing."""

    file_path = request.param
    file_name = file_path.name
    # File_name format - {type}_{chip_count}_{defect}.png
    border_image_path = file_path.parent / ("border_" + file_name)
    border_gray_image_path = file_path.parent / ("gray_" + file_name)

    try:
        base_image = cv2.imread(str(file_path))
        border_image = cv2.imread(str(border_image_path))
        border_gray_image = cv2.cvtColor(
            cv2.imread(str(border_gray_image_path)), cv2.COLOR_BGR2GRAY
        )
        image_arr = {
            "base_file_name": file_name,
            "base": base_image,
            "border": border_image,
            "gray": border_gray_image,
        }
    except:
        pytest.fail(f"Failed to load image {request.param}")
    return image_arr


@pytest.fixture
def sample_batch_config() -> dict[str, tuple[int, int]]:
    """Fixture to provide a sample batch configuration."""
    return {"erode": (5, 5), "close": (37, 37)}


@pytest.fixture
def sample_chip_config() -> dict[str, tuple[int, int]]:
    """Fixture to provide a sample chip configuration."""
    return {"erode": (5, 5), "close": (2, 2)}


@pytest.fixture
def sample_batch_data() -> list[dict[str, float | int]]:
    """Fixture to provide sample batch data for testing."""
    return [
        {"index": 200182.5, "x1": 139, "y1": 110, "x2": 226, "y2": 249},
        {"index": 200360.5, "x1": 308, "y1": 110, "x2": 413, "y2": 245},
        {"index": 200534.0, "x1": 479, "y1": 109, "x2": 589, "y2": 232},
        {"index": 200717.0, "x1": 661, "y1": 112, "x2": 773, "y2": 251},
        {"index": 200895.0, "x1": 835, "y1": 111, "x2": 955, "y2": 254},
        {"index": 400167.0, "x1": 111, "y1": 310, "x2": 223, "y2": 453},
        {"index": 400353.0, "x1": 296, "y1": 310, "x2": 410, "y2": 457},
        {"index": 400533.0, "x1": 472, "y1": 309, "x2": 594, "y2": 448},
        {"index": 400725.5, "x1": 680, "y1": 309, "x2": 771, "y2": 453},
        {"index": 400895.0, "x1": 850, "y1": 309, "x2": 940, "y2": 435},
        {"index": 600175.0, "x1": 113, "y1": 513, "x2": 237, "y2": 655},
        {"index": 600355.5, "x1": 298, "y1": 509, "x2": 413, "y2": 650},
        {"index": 600532.5, "x1": 470, "y1": 518, "x2": 595, "y2": 653},
        {"index": 600720.5, "x1": 663, "y1": 510, "x2": 778, "y2": 634},
        {"index": 600898.5, "x1": 847, "y1": 519, "x2": 950, "y2": 658},
    ]


@pytest.fixture
def sample_clean_contours() -> list[tuple[list, float]]:
    """Fixture to provide sample clean contours data."""
    return [
        ([], 232.5),
        ([], 266.0),
        ([], 237.5),
        ([], 267.0),
        ([], 260.0),
        ([], 267.5),
        ([], 293.5),
        ([], 282.5),
        ([], 249.0),
        ([], 275.5),
        ([], 280.0),
        ([], 228.5),
        ([], 260.0),
        ([], 294.0),
        ([], 300.0),
        ([], 261.5),
        ([], 254.0),
        ([], 269.0),
        ([], 260.0),
        ([], 294.0),
        ([], 254.0),
        ([], 290.0),
        ([], 253.5),
        ([], 300.0),
        ([], 263.5),
        ([], 270.0),
        ([], 257.5),
        ([], 259.5),
        ([], 260.5),
        ([], 248.0),
        ([], 271.5),
        ([], 270.0),
        ([], 303.0),
        ([], 270.0),
        ([], 255.5),
        ([], 287.0),
        ([], 277.0),
        ([], 303.0),
        ([], 280.5),
        ([], 289.0),
        ([], 301.0),
        ([], 300.0),
        ([], 291.5),
        ([], 279.0),
        ([], 280.0),
        ([], 278.5),
        ([], 286.5),
        ([], 269.0),
        ([], 271.0),
        ([], 252.0),
    ]
