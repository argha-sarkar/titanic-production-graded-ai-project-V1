import sys
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split

from src.entity.config_entity import DataTransformationArtifact, DataTransformationConfig, DataValidationArtifact
from src.exception.exception import CustomException
from src.logger.logger import logger
from src.utils.common import create_directories, save_numpy_array, save_object

class DataTransformation:
    def __init__(self, config: DataTransformationConfig, validation_artifact: DataValidationArtifact):
        self.config = config
        self.validation_artifact = validation_artifact

    def _get_feature_lists(self):
        numerical_features = ["Age", "Fare", "SibSp", "Parch", "Pclass"]
        categorical_features = ["Sex", "Embarked"]
        target_column = "Survived"
        return numerical_features, categorical_features, target_column

    def _create_numeric_pipeline(self):
        return Pipeline(steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())])

    def _create_categorical_pipeline(self):
        return Pipeline(steps=[("imputer", SimpleImputer(strategy="most_frequent")), ("encoder", OneHotEncoder(handle_unknown="ignore"))])

    def _build_preprocessor(self) -> ColumnTransformer:
        num, cat, _ = self._get_feature_lists()
        return ColumnTransformer(transformers=[
            ("numerical", self._create_numeric_pipeline(), num),
            ("categorical", self._create_categorical_pipeline(), cat)
        ])

    def _save_artifacts(self, X_train, y_train, X_test, y_test, preprocessor):
        create_directories([Path(self.config.root_dir)])
        save_numpy_array(self.config.X_train_path, X_train)
        save_numpy_array(self.config.y_train_path, y_train)
        save_numpy_array(self.config.X_test_path, X_test)
        save_numpy_array(self.config.y_test_path, y_test)
        save_object(file_path=self.config.preprocessor_path, obj=preprocessor)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logger.info("Starting Data Transformation.")
            df = pd.read_csv(self.validation_artifact.validated_train_file_path)
            
            # Splitting and transforming logic
            num, cat, target = self._get_feature_lists()
            train_df, test_df = train_test_split(df, test_size=self.config.test_size, random_state=self.config.random_state)
            
            preprocessor = self._build_preprocessor()
            X_train = preprocessor.fit_transform(train_df[num + cat])
            X_test = preprocessor.transform(test_df[num + cat])
            
            y_train = train_df[target].to_numpy()
            y_test = test_df[target].to_numpy()

            self._save_artifacts(X_train, y_train, X_test, y_test, preprocessor)
            
            return DataTransformationArtifact(
                X_train_path=self.config.X_train_path,
                y_train_path=self.config.y_train_path,
                X_test_path=self.config.X_test_path,
                y_test_path=self.config.y_test_path,
                preprocessor_path=self.config.preprocessor_path
            )
        except Exception as e:
            raise CustomException(e, sys)