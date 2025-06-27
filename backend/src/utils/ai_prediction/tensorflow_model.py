import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

from pathlib import Path
from tensorflow import keras
from keras import models

from core.exceptions import NoResultsFound
from core.file_manager import FileManager
from utils.debug import error_handler


# TODO: pytest
class TensorflowModel:
    """A utility class for loading and preparing TensorFlow models for prediction."""

    @error_handler()
    @staticmethod
    def load_model(ai_model_path: Path) -> models.Sequential:
        """Loads a Keras Sequential model from a given path.

        Args:
            ai_model_path: The pathlib.Path object pointing to the model file.

        Returns:
            A loaded Keras Sequential model.

        Raises:
            FileNotFoundError: If the model file does not exist.
        """
        ai_model_file_name = ai_model_path.name
        if not ai_model_path.exists():
            raise FileNotFoundError(
                f"{ai_model_file_name} not found in {ai_model_path}"
            )

        return models.load_model(ai_model_path)

    @error_handler()
    @staticmethod
    def save_model(model: models.Sequential, ai_model_path: Path) -> None:
        """Saves a Keras Sequential model to a specified path.

        Args:
            model: The Keras Sequential model to save.
            ai_model_path: The pathlib.Path object pointing to the model file.

        Returns:
            None
        """
        model.save(ai_model_path)

    @error_handler()
    @staticmethod
    def read_class_txt(txt_path: Path) -> dict[str, str]:
        """Reads a text file containing class labels and their corresponding integer keys.

        Args:
            txt_path: The Path object representing the file path of the class labels text file.

        Returns:
            A dictionary where keys are the integer class IDs and values are the string labels.

        Raises:
            NoResultsFound: If the labels file is empty or missing dataset keys.
            ValueError: If a line in the labels file has an invalid format.
        """
        read_data = FileManager.readlines_txt(txt_path)
        if not read_data:
            raise NoResultsFound(
                f"Labels File : {txt_path.name} is empty or is missing dataset keys."
            )

        labels = {}
        for line in read_data:
            strip_txt = line.strip()
            try:
                key, value = strip_txt.split(" ")
                labels[int(key)] = value
            except ValueError as e:
                raise ValueError(
                    f"Labels File: {txt_path.name} has an invalid format at line: {strip_txt}."
                ) from e

        return labels

    @error_handler()
    @staticmethod
    def save_class_txt(dataset_classes: list[str], txt_path: Path) -> None:
        """Saves a list of class labels to a text file, with each label preceded by its index.

        Args:
            dataset_classes: A list of string class labels.
            txt_path: The Path object representing the file path where the class labels will be saved.

        Returns:
            None
        """
        txt_content = "\n".join(
            f"{i} {label}" for i, label in enumerate(dataset_classes)
        )
        FileManager.write_txt(txt_path, txt_content)
