from src.components.data_ingestion import (
    DataIngestion,
)

from src.components.data_validation import (
    DataValidation,
)

from src.config.configuration import (
    ConfigurationManager,
)

from src.logger.logger import (
    logger,
)


class TrainingPipeline:

    def __init__(self):

        self.config = ConfigurationManager()

    def run(self):

        logger.info(
            "Training Pipeline Started."
        )

        ingestion = DataIngestion(

            self.config.get_data_ingestion_config()

        )

        ingestion_artifact = (

            ingestion.initiate_data_ingestion()

        )

        logger.info(
            ingestion_artifact
        )

        validation = DataValidation(

            self.config.get_data_validation_config()

        )

        validation_artifact = (

            validation.initiate_data_validation()

        )

        logger.info(
            validation_artifact
        )

        logger.info(
            "Training Pipeline Completed."
        )


if __name__ == "__main__":

    pipeline = TrainingPipeline()

    pipeline.run()