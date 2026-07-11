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

from src.components.data_transformation import(
    DataTransformation,
)

from src.components.model_trainer import (
    ModelTrainer
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

            config = self.config.get_data_validation_config(),
            ingestion_artifact=ingestion_artifact,

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
        
        transformation = DataTransformation(
            config=self.config.get_data_transformation_config(),
            validation_artifact=validation_artifact,
        )

        transformation_artifact = (
            transformation.initiate_data_transformation()
        )

        logger.info(
            transformation_artifact
        )
        
        
        trainer = ModelTrainer(
            config=self.config.get_model_trainer_config(),
            transformation_artifact=transformation_artifact,
        )

        trainer_artifact = trainer.initiate_model_training()

        logger.info(trainer_artifact)


if __name__ == "__main__":

    pipeline = TrainingPipeline()

    pipeline.run()