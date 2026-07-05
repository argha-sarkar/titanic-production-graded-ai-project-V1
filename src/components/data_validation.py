"""
Production Data Validation Component.
"""

import sys

import pandas as pd

from src.entity.config_entity import (
    DataValidationArtifact,
    DataValidationConfig,
)

from src.exception.exception import (
    CustomException,
)

from src.logger.logger import (
    logger,
)

from src.utils.common import (
    read_yaml,
    write_yaml,
)


class DataValidation:
    """
    Validates the ingested dataset against
    the project schema.
    """

    def __init__(
        self,
        config: DataValidationConfig,
    ) -> None:

        self.config = config

        self.dataset = None

        self.schema = None

        self.validation_report = {}

        self.validation_status = True
        
    
    def _load_dataset(
        self,
    ) -> None:
        """
        Load the ingested training dataset.
        """

        logger.info(
            "Loading training dataset."
        )

        self.dataset = pd.read_csv(
            self.config.train_file_path
        )
        
    def _load_schema(
        self,
    ) -> None:
        """
        Load validation schema.
        """

        logger.info(
            "Loading schema."
        )

        self.schema = read_yaml(
            self.config.schema_file_path
        )
        
    def _initialize_report(
        self,
    ) -> None:

        self.validation_report = {

            "validation_status": True,

            "required_columns": None,

            "missing_columns": [],

            "dtype_validation": None,

            "duplicate_check": None,

            "allowed_values": None,

            "missing_threshold": None,
        }