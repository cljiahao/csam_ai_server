from enum import IntEnum, StrEnum


class DatasetModes(StrEnum):
    NG = "ng"
    GOOD = "good"


class ModelFiles(StrEnum):
    LABEL_EXT = ".txt"
    H5_MODEL_EXT = ".h5"
    KERAS_MODEL_EXT = ".keras"
    ONNX_MODEL_EXT = ".onnx"
    TRAINING_JSON = "training.json"


class ModelStatus(StrEnum):
    AUGMENTED = "augmented"
    TRAINING = "training"
    TRAINED = "trained"
    EVALUATING = "evaluating"
    EVALUATED = "evaluated"
    COMPLETED = "completed"


class HyperParameters(IntEnum):
    BATCH_SIZE: int = 64
    EPOCHS: int = 10000
    SEED: int = 12345
