import torch
import torch.nn as nn
import numpy as np

import core.constants as core_consts
from core.directory import directory
from core.logging import logger
from utils.fileHandle.txt import read_model_txt


def predict_defects(
    item: str, temp_dict: dict[str, np.ndarray]
) -> dict[str, np.ndarray]:
    """Load model, read defect labels and return prediction."""

    model = load_model(item)
    labels = read_model_txt(item)
    results = run_cnn(model, labels, temp_dict)

    return results


def load_model(item: str) -> nn.Module:
    """Load model based on item name."""

    model_f_name = f"{item}.pth"
    model_path = directory.model_dir / model_f_name

    if not model_path.exists():
        std_out = f"Model file: {model_f_name} not found in model folder."
        logger.error(std_out)
        raise FileNotFoundError(std_out)

    # Load the model state dict
    model = torch.load(model_path)
    logger.info(f"Model loaded from {model_path}")

    return model


def run_cnn(
    model: nn.Module, labels: dict[str, str], temp_dict: dict[str, np.ndarray]
) -> dict[str, np.ndarray]:
    """Run model to retrieve predictions."""

    model.eval()  # Ensure the model is in evaluation mode

    # Convert predictions to tensor
    temp_images = np.array(list(temp_dict.values()))
    temp_tensors = torch.tensor(temp_images, dtype=torch.float32)

    # Run the model to get predictions
    with torch.no_grad():  # Disable gradient calculation
        prediction_results = model(temp_tensors).numpy()

    predictions = np.argmax(prediction_results, axis=1)

    # Filter out labels based on settings
    filtered_labels = {k: v for k, v in labels.items() if v not in core_consts.G_TYPES}

    results = {
        k: temp_dict[k]
        for i, k in enumerate(temp_dict.keys())
        if predictions[i] in filtered_labels
    }

    return results
