import cv2
import numpy as np
from tensorflow import keras
from keras import models


from apis.v2.schemas.csam_image import LabeledImageData
from constants.tensorflow_model import DatasetModes, ModelFiles
from core.directory_manager import directory_manager as dm
from utils.ai_prediction.tensorflow_model import TensorflowModel


def run_model_prediction(
    item: str, to_predict_list: list[LabeledImageData]
) -> list[LabeledImageData]:

    model, class_names = setup_evaluation_environment(item)

    images_to_predict = np.array(
        [
            cv2.cvtColor(to_predict.image_data, cv2.COLOR_BGR2RGB)
            for to_predict in to_predict_list
        ]
    )
    prediction_result = model.predict(images_to_predict, batch_size=256, verbose=2)
    predictions = np.argmax(prediction_result, axis=1)

    filtered_labels = {
        k: v for k, v in class_names.items() if v.lower() == DatasetModes.NG
    }

    return [
        to_predict_list[i]
        for i, predict in enumerate(predictions)
        if predict in filtered_labels
    ]


def setup_evaluation_environment(item: str) -> tuple[models.Sequential, dict[str, str]]:
    """Sets up the necessary environments for evaluation."""
    txt_path = dm.model_dir / f"{item}{ModelFiles.LABEL_EXT}"
    model_path = dm.model_dir / f"{item}{ModelFiles.H5_MODEL_EXT}"

    model = TensorflowModel.load_model(model_path)
    labels = TensorflowModel.read_class_txt(txt_path)

    return model, labels
