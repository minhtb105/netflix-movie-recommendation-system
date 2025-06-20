import logging
import numpy as np
from abc import ABC, abstractmethod

class Evaluation(ABC):
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray):
        """
        Calculate the scores for the model
        Args:
            y_true: True labels
            y_pred: predicted labels
        Returns:
            None
        """
        pass