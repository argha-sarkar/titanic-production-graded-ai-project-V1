from src.components.data_ingestion import (
    DataIngestion,
)

from src.config.configuration import (
    ConfigurationManager,
)


def test_data_ingestion():

    manager = ConfigurationManager()

    config = manager.get_data_ingestion_config()

    component = DataIngestion(config)

    artifact = component.initiate_data_ingestion()

    assert artifact.train_file_path.exists()

    assert artifact.test_file_path.exists()