"""
Configuration Manager
"""

from pathlib import Path

import yaml

from src.constants import (
    CONFIG_FILE_PATH,
    SCHEMA_FILE_PATH,
)

from src.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    LoggingConfig,
)


class ConfigurationManager:

    def __init__(self):

        self.config = self._read_yaml(
            CONFIG_FILE_PATH
        )

    @staticmethod
    def _read_yaml(file_path: Path):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as yaml_file:

            return yaml.safe_load(
                yaml_file
            )

    
    def get_data_ingestion_config(
    self
    ) -> DataIngestionConfig:

        artifact_config = self.config["artifacts"]["data_ingestion"]

        data_config = self.config["data"]

        return DataIngestionConfig(

            root_dir=Path(
                artifact_config["root_dir"]
            ),

            raw_train_data_path=Path(
                data_config["train_data_path"]
            ),

            raw_test_data_path=Path(
                data_config["test_data_path"]
            ),

            ingested_train_path=Path(
                artifact_config["train_file"]
            ),

            ingested_test_path=Path(
                artifact_config["test_file"]
            )
        )
        
        

    def get_data_validation_config(
        self
    ) -> DataValidationConfig:

        config = self.config["artifacts"]["data_validation"]

        return DataValidationConfig(

            root_dir=Path(
                config["root_dir"]
            ),

            validation_report_file_path=Path(
                config["validation_report"]
            ),

            validation_status_file_path=Path(
                config["validation_status"]
            ),

            schema_file_path=SCHEMA_FILE_PATH,
        )

    def get_data_transformation_config(
        self
    ) -> DataTransformationConfig:

        config = self.config["artifacts"]["data_transformation"]

        return DataTransformationConfig(

            root_dir=Path(
                config["root_dir"]
            ),

            train_array_path=Path(
                config["train_array"]
            ),

            test_array_path=Path(
                config["test_array"]
            ),

            preprocessor_path=Path(
                config["preprocessor"]
            ),
        )

    def get_model_trainer_config(
        self
    ) -> ModelTrainerConfig:

        config = self.config["artifacts"]["model_trainer"]

        return ModelTrainerConfig(

            root_dir=Path(
                config["root_dir"]
            ),

            trained_model_path=Path(
                config["trained_model"]
            ),
        )
        
    def get_logging_config(
        self
    ) -> LoggingConfig:

        config = self.config["logging"]

        return LoggingConfig(

        log_level=config["level"],

        log_dir=Path(config["log_dir"])

    )
        
    