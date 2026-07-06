from src.config.configuration import ConfigurationManager
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation


def test_data_transformation():

    manager = ConfigurationManager()

    ingestion = DataIngestion(
        manager.get_data_ingestion_config()
    )

    ingestion_artifact = (
        ingestion.initiate_data_ingestion()
    )

    validation = DataValidation(
        config=manager.get_data_validation_config(),
        ingestion_artifact=ingestion_artifact,
    )

    validation_artifact = (
        validation.initiate_data_validation()
    )

    transformation = DataTransformation(
        config=manager.get_data_transformation_config(),
        validation_artifact=validation_artifact,
    )

    artifact = (
        transformation.initiate_data_transformation()
    )

    assert artifact.train_array_path.exists()
    assert artifact.test_array_path.exists()
    assert artifact.preprocessor_path.exists()