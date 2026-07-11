from src.components.data_validation import DataValidation
from src.components.data_ingestion import DataIngestion
from src.config.configuration import ConfigurationManager

def test_data_validation():
    manager = ConfigurationManager()

    # 1. Properly initialize and execute Data Ingestion to define the artifact
    ingestion_config = manager.get_data_ingestion_config()
    ingestion = DataIngestion(config=ingestion_config)
    
    # This line defines the 'ingestion_artifact' variable
    ingestion_artifact = ingestion.initiate_data_ingestion()

    # 2. Now use that defined variable to initialize DataValidation
    config = manager.get_data_validation_config()
    validator = DataValidation(
    config=config,
    ingestion_artifact=ingestion_artifact  # Correct argument name
)

    # 3. Run validation
    artifact = validator.initiate_data_validation()

    # 4. Assertions
    assert artifact.report_file_path.exists()
    assert artifact.status_file_path.exists()
    assert isinstance(artifact.validation_status, bool)