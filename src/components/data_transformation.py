"""
Production Data Transformation Component.
"""

import sys

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer

from sklearn.impute import SimpleImputer

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
)

from src.entity.config_entity import (
    DataTransformationArtifact,
    DataTransformationConfig,
    DataValidationArtifact,
)

from src.exception.exception import (
    CustomException,
)

from src.logger.logger import logger

from src.utils.common import (
    create_directories,
    save_numpy_array,
    save_object,
)


class DataTransformation:
    """
    Prepare validated data for model training.
    """

    def __init__(
        self,
        config: DataTransformationConfig,
        validation_artifact: DataValidationArtifact,
    ) -> None:

        self.config = config

        self.validation_artifact = validation_artifact
        
        
    @staticmethod
    def _get_feature_lists():

        numerical_features = [

            "Age",

            "Fare",

            "SibSp",

            "Parch",

            "Pclass",

        ]

        categorical_features = [

            "Sex",

            "Embarked",

        ]

        target_column = "Survived"

        return (

            numerical_features,

            categorical_features,

            target_column,

        )
        
    @staticmethod
    def _create_numeric_pipeline():

        return Pipeline(

            steps=[

                (

                    "imputer",

                    SimpleImputer(

                        strategy="median"

                    ),

                ),

                (

                    "scaler",

                    StandardScaler(),

                ),

            ]

        )