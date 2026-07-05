from src.components.data_validation import (
    DataValidation,
)

from src.config.configuration import (
    ConfigurationManager,
)


def test_data_validation():

    manager = ConfigurationManager()

    config = manager.get_data_validation_config()

    validator = DataValidation(config)

    artifact = validator.initiate_data_validation()

    assert artifact.report_file_path.exists()

    assert artifact.status_file_path.exists()

    assert isinstance(
        artifact.validation_status,
        bool,
    )