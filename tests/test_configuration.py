from src.config.configuration import (
    ConfigurationManager
)


def test_load_config():

    config = ConfigurationManager()

    assert config.get_config() is not None


def test_load_schema():

    config = ConfigurationManager()

    assert config.get_schema() is not None