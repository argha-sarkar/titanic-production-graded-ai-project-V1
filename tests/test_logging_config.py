from src.config.configuration import (
    ConfigurationManager
)


def test_logging_config():

    manager = ConfigurationManager()

    config = manager.get_logging_config()

    assert config.log_level == "INFO"