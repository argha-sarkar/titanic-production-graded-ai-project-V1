from src.components.data_validation import (
    DataValidation,
)

from src.config.configuration import (
    ConfigurationManager,
)


manager = ConfigurationManager()

config = manager.get_data_validation_config()

validator = DataValidation(config)

artifact = validator.initiate_data_validation()

print(artifact)