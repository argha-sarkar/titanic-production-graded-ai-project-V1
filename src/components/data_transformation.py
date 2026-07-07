"""
Production Data Transformation Component.
"""

import sys
from pathlib import Path


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

from sklearn.model_selection import (
    train_test_split,
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
        train_df: pd.DataFrame,
        test_df: pd.DataFrame,
    ):
        """"
        Fit the preprocessor on the training data and 
        transform both training and testing data.
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
        
        X_train = train_df[
            feature_columns
        ]
        
        y_train = train_df[
            target_column
        ]
        
        x_test = test_df[
            feature_columns
        ]
        
        y_test = test_df[
            target_column
        ]
        
        preprocessor = self._build_preprocessor()
        
        X_train = preprocessor.fit_transform(
            X_train
        )
        
        X_test = preprocessor.transform(
            x_test
        )
        
        train_array = np.c_[
            X_train,
            y_train.to_numpy()
        ]
        
        test_array = np.c_[
            X_test,
            y_test.to_numpy(),
        ]
        
        return (
            X_train,
            y_train.to_numpy(),
            X_test,
            y_test.to_numpy(),
            preprocessor,
        )
    
    
    def _split_dataset(
        self,
        dataframe: pd.DataFrame,
    ):
        
        """
        Split dataset into training and testing sets.
        """
        
        logger.info(
            "Spliting dataset"
        )
        
        return train_test_split(
            dataframe,
            test_size = self.config.test_size,
            random_state = self.config.random_state,
            stratify=dataframe[
                self.config.target_column
                ], 
        )
    
    def _save_artifacts(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_test: np.ndarray,
        y_test: np.ndarray,
        preprocessor: ColumnTransformer,
    ) -> None:
        """
        Save the transformed data arrays and the preprocessor object.
        """
        # Ensure the directory exists
        create_directories([Path(self.config.root_dir)])

        # Save the train and test arrays
        save_numpy_array(
            file_path=self.config.X_train_path,
            array=X_train,
        )

        save_numpy_array(
            file_path=self.config.y_train_path,
            array=y_train,
        )

        save_numpy_array(
            file_path=self.config.X_test_path,
            array=X_test,
        )

        save_numpy_array(
            file_path=self.config.y_test_path,
            array=y_test,
        )

        # Save the preprocessor object
        save_object(
            file_path=self.config.preprocessor_path,
            obj=preprocessor,
        )
        
    
    def initiate_data_transformation(
    self,
    ) -> DataTransformationArtifact:
        """
        Execute the complete data transformation pipeline.
        """

        try:

            logger.info(
                "Starting Data Transformation."
            )

            dataframe = self._load_dataset()

            train_df, test_df = self._split_dataset(
                dataframe
            )

            (
                X_train,
                y_train,
                X_test,
                y_test,
                preprocessor,
            ) = self._fit_transform(
                train_df,
                test_df,
            )

            self._save_artifacts(
                X_train,
                y_train,
                X_test,
                y_test,
                preprocessor,
            )

            logger.info(
                "Data Transformation Completed."
            )

            return DataTransformationArtifact(

                X_train_path=self.config.X_train_path,

                y_train_path=self.config.y_train_path,

                X_test_path=self.config.X_test_path,

                y_test_path=self.config.y_test_path,

                preprocessor_path=self.config.preprocessor_path,

            )

        except Exception as error:

            logger.exception(
                "Data Transformation Failed."
            )

            raise CustomException(
                error,
                sys,
            )
            
            
    @staticmethod
    def _create_categorical_pipeline():
        return Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("encoder", OneHotEncoder(handle_unknown="ignore")),
            ]
        )