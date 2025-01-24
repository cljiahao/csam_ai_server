import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import cv2
import numpy as np
from keras import models, Sequential
from tensorflow import keras

from core.directory import directory
from core.logging import logger
from core.exceptions import CustomErrorMessage
from schemas.chips_data import ImageData


class TFPrediction:
    """
    Handles TensorFlow model prediction tasks, including model loading, label reading, and inference.

    Args:
        item (str): The base name of the model and label files (without extensions).

    Attributes:
        model_name (str): The name of the model file.
        txt_name (str): The name of the label file.
        labels (dict[str, str]): Mapping of class indices to labels.
        model (Sequential): The TensorFlow/Keras model used for predictions.
    """

    def __init__(self, item: str) -> None:
        self.model_name = f"{item}.h5"
        self.txt_name = f"{item}.txt"
        self.labels = self._read_model_mode()
        self.model = self._load_model_file()

    def _read_model_mode(self) -> dict[str, str]:
        """Reads and parses the label file to create a mapping of class indices to labels."""

        txt_path = directory.model_dir / self.txt_name
        if not txt_path.exists():
            raise CustomErrorMessage(
                f"Model File: {self.txt_name} not found in the model folder."
            )

        with open(txt_path, "r") as f:
            read_data = f.readlines()

        if not read_data:
            raise CustomErrorMessage(
                f"Labels File : {txt_path.name} is empty or is missing dataset keys."
            )

        labels = {}
        for line in read_data:
            strip_txt = line.strip()
            try:
                key, value = strip_txt.split(" ")
                labels[key] = value
            except ValueError as e:
                raise CustomErrorMessage(
                    f"Labels File: {txt_path.name} has an invalid format at line: {strip_txt}."
                ) from e

            return labels

    def _load_model_file(self) -> Sequential:
        """Loads the TensorFlow/Keras model from the file system."""
        model_path = directory.model_dir / self.model_name
        if not model_path.exists():
            raise CustomErrorMessage(
                f"Model File: {self.model_name} not found in model folder."
            )

        model = models.load_model(model_path)
        logger.info(f"Model loaded from {model_path}")
        return model

    def write_model_mode(self, labels: list[str]) -> None:
        """Writes a list of labels to the label file."""
        txt_path = directory.model_dir / self.txt_name

        label_content = "\n".join(f"{i} {label}" for i, label in enumerate(labels))

        with open(txt_path, "w") as f:
            f.write(label_content)

        logger.info(f"Label file '{txt_path}' written successfully.")

    def run_model_CNN(self, to_predict_list: list[ImageData]) -> list[ImageData]:
        """Runs predictions on a list of images and filters the results based on labels."""
        images_to_predict = np.array(
            [
                cv2.cvtColor(to_predict.rotated_image, cv2.COLOR_BGR2RGB)
                for to_predict in to_predict_list
            ]
        )
        prediction_result = self.model.predict(
            images_to_predict, batch_size=256, verbose=2
        )
        predictions = np.argmax(prediction_result, axis=1)

        # Filter out labels based on settings
        filtered_labels = {
            k: v for k, v in self.labels.items() if v.lower() not in ["g", "good"]
        }

        results = [
            to_predict_list[i]
            for i, predict in enumerate(predictions)
            if str(predict) in filtered_labels
        ]

        return results
