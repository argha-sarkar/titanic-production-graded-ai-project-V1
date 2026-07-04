from src.constants import (
    CONFIG_FILE_PATH,
    SCHEMA_FILE_PATH,
    ARTIFACT_DIR,
)


def test_config_path():

    assert CONFIG_FILE_PATH.exists()


def test_schema_path():

    assert SCHEMA_FILE_PATH.exists()


def test_artifact_directory():

    assert ARTIFACT_DIR.exists()