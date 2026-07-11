"""
Production Model Trainer.
"""

import json
import sys

import pandas as pd

from sklearn.ensemble import (
    GradientBoostingClassifier,
    RandomForestClassifier,
)

from sklearn.linear_model import (
    LogisticRegression,
)

from sklearn.model_selection import (
    cross_val_score,
)

from sklearn.tree import (
    DecisionTreeClassifier,
)

from src.entity.config_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact,
    ModelTrainerConfig,
)

from src.exception.exception import (
    CustomException,
)

from src.logger.logger import logger

from src.utils.common import (
    load_numpy_array,
    save_object,
    create_directories,
)


class ModelTrainer:
    """
    Train and compare multiple ML models.
    """

    def __init__(
        self,
        config: ModelTrainerConfig,
        transformation_artifact: DataTransformationArtifact,
    ) -> None:

        self.config = config

        self.transformation_artifact = transformation_artifact
    
    
# ==========================================================
# Load Dataset
# ==========================================================   
        
        
    def _load_dataset(
        self,
    ):

        logger.info(
            "Loading transformed datasets."
        )

        X_train = load_numpy_array(
            self.transformation_artifact.X_train_path
        )

        y_train = load_numpy_array(
            self.transformation_artifact.y_train_path
        )

        X_test = load_numpy_array(
            self.transformation_artifact.X_test_path
        )

        y_test = load_numpy_array(
            self.transformation_artifact.y_test_path
        )

        return (

            X_train,

            y_train,

            X_test,

            y_test,

        )
        
        
# ==========================================================
# Create Candidate Models
# ==========================================================

    def _get_models(
        self,
    ):

        return {

            "Logistic Regression":

                LogisticRegression(

                    random_state=self.config.random_state,

                    max_iter=1000,

                ),

            "Decision Tree":

                DecisionTreeClassifier(

                    random_state=self.config.random_state,

                ),

            "Random Forest":

                RandomForestClassifier(

                    random_state=self.config.random_state,

                ),

            "Gradient Boosting":

                GradientBoostingClassifier(

                    random_state=self.config.random_state,

                ),

        }