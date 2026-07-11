from src.config.configuration import ConfigurationManager
from src.components.model_trainer import ModelTrainer

# Import previous components to build artifacts
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation


def test_model_trainer():

    manager = ConfigurationManager()

    ingestion = DataIngestion(
        manager.get_data_ingestion_config()
    )

    ingestion_artifact = ingestion.initiate_data_ingestion()

    validation = DataValidation(
        config=manager.get_data_validation_config(),
        ingestion_artifact=ingestion_artifact,
    )

    validation_artifact = validation.initiate_data_validation()

    transformation = DataTransformation(
        config=manager.get_data_transformation_config(),
        validation_artifact=validation_artifact,
    )

    transformation_artifact = (
        transformation.initiate_data_transformation()
    )

    trainer = ModelTrainer(
        config=manager.get_model_trainer_config(),
        transformation_artifact=transformation_artifact,
    )

    artifact = trainer.initiate_model_training()

    assert artifact.best_model_path.exists()
    assert artifact.metrics_path.exists()
    assert artifact.leaderboard_path.exists()