import os
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from fastapi import HTTPException

from apis.utils.directory import dire
from core.config import Settings
from core.read_write import read_txt


class CSAM_model(nn.Module):
    def __init__(self):
        super(CSAM_model, self).__init__()
        self.rescaling = nn.Identity()
        self.random_flip = nn.Identity()

        # Convolutional layers
        self.conv1 = nn.Conv2d(3, 32, kernel_size=(3, 3), padding="same")
        self.bn1 = nn.BatchNorm2d(32)

        self.conv2 = nn.Conv2d(32, 64, kernel_size=(3, 3), padding="same")
        self.bn2 = nn.BatchNorm2d(64)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv3 = nn.Conv2d(64, 128, kernel_size=(3, 3), padding="same")
        self.bn3 = nn.BatchNorm2d(128)

        self.conv4 = nn.Conv2d(128, 256, kernel_size=(3, 3), padding="same")
        self.bn4 = nn.BatchNorm2d(256)
        self.pool2 = nn.MaxPool2d(kernel_size=3, stride=2)

        self.conv5 = nn.Conv2d(256, 512, kernel_size=(3, 3), padding="same")
        self.bn5 = nn.BatchNorm2d(512)

        self.conv6 = nn.Conv2d(512, 1024, kernel_size=(3, 3), padding="same")
        self.bn6 = nn.BatchNorm2d(1024)

        # Pooling, flattening, and fully connected layers
        self.avg_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.dropout = nn.Dropout(0.4)
        self.fc = nn.Linear(1024, 4)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Forward pass through Conv layers with batch normalization and ReLU activation
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = self.pool1(x)

        x = F.relu(self.bn3(self.conv3(x)))
        x = F.relu(self.bn4(self.conv4(x)))
        x = self.pool2(x)

        x = F.relu(self.bn5(self.conv5(x)))
        x = F.relu(self.bn6(self.conv6(x)))

        # Global average pooling and flattening
        x = self.avg_pool(x)
        x = torch.flatten(x, 1)  # Flatten but keep the batch dimension

        # Dropout and final fully connected layer
        x = self.dropout(x)
        x = self.fc(x)

        return x


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
    model_path = os.path.join(dire.model_path, f"{item}.pth")
    if not os.path.exists(model_path):
        raise HTTPException(
            status_code=522,
            detail=f"Model File: {item}.pth not found in model folder",
        )
    model = CSAM_model()
    model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))
    model.eval()

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
    pred_tensor = torch.tensor(pred_arr).float()
    pred_tensor = pred_tensor.permute(
        0, 3, 1, 2
    )  # Convert (batch, H, W, C) to (batch, C, H, W)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    pred_tensor = pred_tensor.to(device)

    # Run the prediction in a no_grad block to avoid tracking gradients
    with torch.no_grad():
        # Get model predictions
        outputs = model(pred_tensor)

        # Get predicted class indices using argmax
        pred_res = torch.argmax(outputs, dim=1).cpu().numpy()

    # Load labels for the chip item
    labels_path = os.path.join(dire.model_path, f"{item}.txt")
    data = read_txt(labels_path)

    # Remove any labels in the settings.G_TYPES list
    for key in list(data.keys()):
        if data[key] in Settings.G_TYPES:
            del data[key]

    # Get keys for the NG class
    ng_key = data.keys()

    # Filter the results based on the predicted classes
    res = {
        k: pred_dict[k]
        for (i, k) in enumerate(list(pred_dict.keys()))
        if str(pred_res[i]) in ng_key
    }

    return res
