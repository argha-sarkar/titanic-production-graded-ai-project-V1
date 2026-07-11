"""
Model training engine.
"""

import numpy as np

from sklearn.base import ClassifierMixin


class ModelTrainerEngine:
    """
    Train a machine learning model and generate predictions.
    """

    @staticmethod
    def train(
        model: ClassifierMixin,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_test: np.ndarray,
    ):
        """
        Train a model and return predictions.
        """

        model.fit(
            X_train,
            y_train,
        )

        predictions = model.predict(
            X_test,
        )

        return model, predictions