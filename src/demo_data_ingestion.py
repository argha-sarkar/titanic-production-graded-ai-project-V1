from src.components.data_ingestion import (
    DataIngestion,
)

from src.config.configuration import (
    ConfigurationManager,
)


manager = ConfigurationManager()

config = manager.get_data_ingestion_config()

component = DataIngestion(config)

artifact = component.initiate_data_ingestion()

print(artifact)