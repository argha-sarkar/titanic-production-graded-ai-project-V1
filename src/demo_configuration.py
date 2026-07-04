from src.config.configuration import (
    ConfigurationManager
)


manager = ConfigurationManager()

config = manager.get_data_ingestion_config()

print(config)

print()

print(config.train_file_path)

print(config.test_file_path)