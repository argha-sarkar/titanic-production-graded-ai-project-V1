"""
Production Data Validation Component.
"""

import sys

import pandas as pd

from src.entity.config_entity import (
    DataIngestionArtifact,
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
        ingestion_artifact: DataIngestionArtifact,
    ) -> None:

        self.config = config

        self.ingestion_artifact = ingestion_artifact

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
            self.ingestion_artifact.train_file_path
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
        
    def _check_required_columns(
        self,
    ) -> None:
        """
        Check whether all required columns exist.
        """

        logger.info(
            "Checking required columns."
        )

        required_columns = self.schema[
            "required_columns"
        ]

        missing_columns = []

        for column in required_columns:

            if column not in self.dataset.columns:

                missing_columns.append(column)

        if missing_columns:

            self.validation_status = False

            self.validation_report[
                "required_columns"
            ] = "FAILED"

            self.validation_report[
                "missing_columns"
            ] = missing_columns

        else:

            self.validation_report[
                "required_columns"
            ] = "PASSED"  
            
    
    def _check_data_types(
        self,
    ) -> None:
        """
        Validate dataset column data types.
        """

        logger.info(
            "Checking data types."
        )

        errors = []

        schema_columns = self.schema["columns"]

        for column, details in schema_columns.items():

            if column not in self.dataset.columns:
                continue

            actual_dtype = str(
                self.dataset[column].dtype
            )

            expected_dtype = details["dtype"]

            if actual_dtype != expected_dtype:

                errors.append(

                    {
                        "column": column,
                        "expected": expected_dtype,
                        "actual": actual_dtype,
                    }

                )

        if errors:

            self.validation_status = False

            self.validation_report[
                "dtype_validation"
            ] = errors

        else:

            self.validation_report[
                "dtype_validation"
            ] = "PASSED"  
            
            
    def _check_allowed_values(
        self,
    ) -> None:
        """
        Validate categorical values.
        """

        logger.info(
            "Checking categorical values."
        )

        allowed = self.schema.get(
            "allowed_values",
            {}
        )

        invalid = {}

        for column, valid_values in allowed.items():

            if column not in self.dataset.columns:
                continue

            observed = (
                self.dataset[column]
                .dropna()
                .unique()
            )

            bad_values = [

                value

                for value in observed

                if value not in valid_values

            ]

            if bad_values:

                invalid[column] = bad_values

        if invalid:

            self.validation_status = False

            self.validation_report[
                "allowed_values"
            ] = invalid

        else:

            self.validation_report[
                "allowed_values"
            ] = "PASSED"
            
    
    def _check_duplicates(
        self,
    ) -> None:
        """
        Check duplicate PassengerId.
        """

        logger.info(
            "Checking duplicates."
        )

        primary_key = self.schema[
            "primary_key"
        ][0]

        duplicates = self.dataset[
            self.dataset[
                primary_key
            ].duplicated()
        ]

        if not duplicates.empty:

            self.validation_status = False

            self.validation_report[
                "duplicate_check"
            ] = duplicates[
                primary_key
            ].tolist()

        else:

            self.validation_report[
                "duplicate_check"
            ] = "PASSED"
            
            
    def _check_missing_threshold(
        self,
    ) -> None:
        """
        Check missing value percentage.
        """

        logger.info(
            "Checking missing thresholds."
        )

        thresholds = self.schema[
            "missing_value_threshold"
        ]

        failures = {}

        for column, threshold in thresholds.items():

            if column not in self.dataset.columns:
                continue

            percentage = (

                self.dataset[column]

                .isnull()

                .mean()

                * 100

            )

            if percentage > threshold:

                failures[column] = {

                    "threshold": threshold,

                    "actual": round(
                        percentage,
                        2,
                    ),
                }

        if failures:

            self.validation_status = False

            self.validation_report[
                "missing_threshold"
            ] = failures

        else:

            self.validation_report[
                "missing_threshold"
            ] = "PASSED"     
            
    
            
    def _save_validation_report(
        self,
    ) -> None:
        """
        Save validation report and status.
        """

        self.validation_report[
            "validation_status"
        ] = self.validation_status

        write_yaml(
            self.config.validation_report_file_path,
            self.validation_report,
        )

        self.config.validation_status_file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.config.validation_status_file_path.write_text(
            str(self.validation_status),
            encoding="utf-8",
        )
          
    
    def initiate_data_validation(
        self,
    ) -> DataValidationArtifact:
        """
        Execute all validation steps.
        """

        try:

            logger.info(
                "Starting Data Validation."
            )

            self._load_dataset()

            self._load_schema()

            self._initialize_report()

            self._check_required_columns()

            self._check_data_types()

            self._check_allowed_values()

            self._check_duplicates()

            self._check_missing_threshold()

            self._save_validation_report()

            logger.info(
                "Data Validation Completed."
            )

            return DataValidationArtifact(

                validation_status=self.validation_status,

                report_file_path=self.config.validation_report_file_path,

                status_file_path=self.config.validation_status_file_path,

            )

        except Exception as error:

            logger.exception(
                "Data Validation Failed."
            )

            raise CustomException(
                error,
                sys,
            )