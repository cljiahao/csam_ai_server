import os
import numpy as np
from tensorflow import keras
from keras import models
from fastapi import HTTPException

from apis.utils.directory import dire
from core.config import settings
from core.read_write import read_txt


def prediction(item, pred_dict):
    """
    Main function to call sub functions for predicting defective chips

    Parameters
    ----------
    item : str
        Chip item full name to retrieve AI model for it
    pred_dict : dict
        Images stored in dictionary for AI to predict

    Returns
    -------
    result : dict
        Prediction results images stored in dictionary
    """
    model = load_model(item)
    result = run_CNN(model, item, pred_dict)

    return result


def load_model(item):
    """
    Parameters
    ----------
    item : str
        Chip item full name to retrieve AI model for it

    Returns
    -------
    model : keras model instance
        Keras model instance for prediction
    """
    model_path = os.path.join(dire.model_path, f"{item}.h5")
    if not os.path.exists(model_path):
        raise HTTPException(
            status_code=522,
            detail=f"Model File: {item}.h5 not found in model folder",
        )
    model = models.load_model(model_path)

    return model


def run_CNN(model, item, pred_dict):
    """
    Parameters
    ----------
    model : keras model instance
        Keras model instance for prediction
    item : str
        Chip item full name to retrieve AI model for it
    pred_dict : dict
        Images stored in dictionary for AI to predict

    Returns
    -------
    pred_dict : dict
        Prediction results images stored in dictionary
    """
    pred_arr = np.array(list(pred_dict.values()))
    pred_res = np.argmax(model.predict(pred_arr, batch_size=256, verbose=2), axis=1)

    labels_path = os.path.join(dire.model_path, f"{item}.txt")
    data = read_txt(labels_path)

    for key in data.keys():
        if key in settings.G_TYPES:
            del data[key]

    res = {
        k: pred_dict[k]
        for (i, k) in enumerate(list(pred_dict.keys()))
        if pred_res[i] in data.keys()
    }

    return res
