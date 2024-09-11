import numpy as np
from tensorflow import keras
from keras import models, Sequential

import core.constants as core_consts
from core.directory import directory
from core.logging import logger
from utils.fileHandle.txt import read_model_txt


def predict_defects(
    item: str, temp_dict: dict[str, np.ndarray]
) -> dict[str, np.ndarray]:
    """Load Model, read defect labels and return prediction."""

    model = load_model(item)
    labels = read_model_txt(item)
    results = run_CNN(model, labels, temp_dict)

    return results


def load_model(item: str) -> Sequential:
    """Load Model based on item name."""

    model_f_name = f"{item}.h5"
    model_path = directory.model_dir / model_f_name

    if not model_path.exists():
        std_out = f"Model File: {model_f_name} not found in model folder"
        logger.error(std_out)
        raise FileNotFoundError(std_out)

    model = models.load_model(model_path)
    logger.info(f"Model loaded from {model_path}")

    return model


def run_CNN(
    model: Sequential, labels: dict[str, str], temp_dict: dict[str, np.ndarray]
) -> dict[str, np.ndarray]:
    """Run model to retrieve prediction."""

    temp_images = np.array(list(temp_dict.values()))
    prediction_results = model.predict(temp_images, batch_size=256, verbose=2)
    predictions = np.argmax(prediction_results, axis=1)

    # Filter out labels based on settings
    filtered_labels = {k: v for k, v in labels.items() if v not in core_consts.G_TYPES}

    results = {
        k: temp_dict[k]
        for i, k in enumerate(temp_dict.keys())
        if predictions[i] in filtered_labels
    }

    return results
