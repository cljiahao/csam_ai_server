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
    model: nn.Module, labels: dict[str, str], pred_dict: dict[str, np.ndarray]
) -> dict[str, np.ndarray]:
    """Run model to retrieve predictions."""

    model.eval()  # Ensure the model is in evaluation mode

    # Convert predictions to tensor
    pred_arr = np.array(list(pred_dict.values()))
    pred_tensor = torch.tensor(pred_arr, dtype=torch.float32)

    # Run the model to get predictions
    with torch.no_grad():  # Disable gradient calculation
        predictions = model(pred_tensor).numpy()

    pred_res = np.argmax(predictions, axis=1)

    # Filter out labels based on settings
    filtered_labels = {k: v for k, v in labels.items() if k not in core_consts.G_TYPES}

    results = {
        k: pred_dict[k]
        for i, k in enumerate(pred_dict.keys())
        if pred_res[i] in filtered_labels
    }

    return results
