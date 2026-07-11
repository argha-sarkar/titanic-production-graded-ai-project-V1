import os
from src.components.data_transformation import DataTransformation
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.config.configuration import ConfigurationManager

def test_data_transformation():
    manager = ConfigurationManager()
    
    # Chain components for integration test
    ingestion = DataIngestion(manager.get_data_ingestion_config())
    ingestion_artifact = ingestion.initiate_data_ingestion()
    
    validation = DataValidation(manager.get_data_validation_config(), ingestion_artifact)
    validation_artifact = validation.initiate_data_validation()
    
    transformation = DataTransformation(manager.get_data_transformation_config(), validation_artifact)
    artifact = transformation.initiate_data_transformation()

    # Assertions
    assert os.path.exists(artifact.X_train_path)
    assert os.path.exists(artifact.y_train_path)
    assert os.path.exists(artifact.X_test_path)
    assert os.path.exists(artifact.y_test_path)
    assert os.path.exists(artifact.preprocessor_path)