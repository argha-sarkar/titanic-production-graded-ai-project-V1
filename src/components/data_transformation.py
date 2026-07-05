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

        self.validation_artifact =validation_artifact
        
        
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
        
    def _build_preprocessor(self) -> ColumnTransformer:
        """
        Build the complete preprocessing pipeline.
        """

        (
            numerical_features,
            categorical_features,
            _,
        ) = self._get_feature_lists()

        preprocessor = ColumnTransformer(

            transformers=[

                (
                    "numerical",

                    self._create_numeric_pipeline(),

                    numerical_features,

                ),

                (
                    "categorical",

                    self._create_categorical_pipeline(),

                    categorical_features,

                ),

            ]

        )

        return preprocessor
    
    
    def _load_dataset(self) -> pd.DataFrame:
        """
        Load the validated dataset.
        """

        logger.info(
            "Loading validated dataset."
        )

        return pd.read_csv(
            self.validation_artifact.validated_train_file_path
        )
        
        
    def _split_features_target(
        self,
        dataframe: pd.DataFrame,
    ):
    
        """
        Split features and target column.
        """

        (
            numerical_features,
            categorical_features,
            target_column,
        ) = self._get_feature_lists()

        feature_columns = (

            numerical_features +

            categorical_features

        )

        X = dataframe[
            feature_columns
        ]

        y = dataframe[
            target_column
        ]

        return X, y
    
    
    def _fit_transform(
        self,
        X: pd.DataFrame,
    ):
        """
        Fit and transform features.
        """

        logger.info(
            "Fitting preprocessing pipeline."
        )

        preprocessor = self._build_preprocessor()

        transformed = preprocessor.fit_transform(X)

        return transformed, preprocessor