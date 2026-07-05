"""
Production Data Ingestion Component.
"""

from pathlib import Path
import shutil
import sys

from src.entity.config_entity import (
    DataIngestionArtifact,
    DataIngestionConfig,
)

from src.exception.exception import (
    CustomException,
)

from src.logger.logger import logger

from src.utils.common import (
    create_directories,
)


class DataIngestion:
    """
    Copies the raw dataset into the artifact directory.
    """

    def __init__(
        self,
        config: DataIngestionConfig,
    ) -> None:

        self.config = config

    def _create_output_directory(
        self,
    ) -> None:

        logger.info(
            "Creating artifact directory."
        )

        create_directories(
            [
                self.config.root_dir
            ]
        )

    def _copy_file(
        self,
        source: Path,
        destination: Path,
    ) -> None:

        if not source.exists():

            raise FileNotFoundError(
                f"{source} not found."
            )

        shutil.copy2(
            source,
            destination
        )

        logger.info(
            "%s copied to %s",
            source,
            destination
        )

    def initiate_data_ingestion(
        self,
    ) -> DataIngestionArtifact:

        try:

            logger.info(
                "Starting Data Ingestion."
            )

            self._create_output_directory()

            self._copy_file(

                self.config.raw_train_data_path,

                self.config.ingested_train_path,

            )

            self._copy_file(

                self.config.raw_test_data_path,

                self.config.ingested_test_path,

            )

            logger.info(
                "Data Ingestion Completed."
            )

            return DataIngestionArtifact(

                train_file_path=self.config.ingested_train_path,

                test_file_path=self.config.ingested_test_path,

            )

        except Exception as error:

            logger.exception(
                "Data Ingestion Failed."
            )

            raise CustomException(
                error,
                sys
            )