"""
Production Data Ingestion Component.
"""

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
    Responsible for reading the raw dataset
    and storing copies in the artifact directory.
    """

    def __init__(
        self,
        config: DataIngestionConfig,
    ) -> None:

        self.config = config
        
    
    def _create_output_directory(
        self,
    ) -> None:
        
        """
        Create the artifact directory.
        """

        logger.info(
            "Creating data ingestion directory."
        )

        create_directories(
            [
                self.config.root_dir,
            ]
        )