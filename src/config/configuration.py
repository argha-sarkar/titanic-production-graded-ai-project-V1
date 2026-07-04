"""
Configuration Manager

Loads project configuration files.
"""

from pathlib import Path

import yaml

from src.constants import (
    CONFIG_FILE_PATH,
    SCHEMA_FILE_PATH
)


class ConfigurationManager:

    """
    Reads all project configuration files.
    """

    def __init__(self):

        self.config = self.read_yaml(
            CONFIG_FILE_PATH
        )

        self.schema = self.read_yaml(
            SCHEMA_FILE_PATH
        )

    @staticmethod
    def read_yaml(
        file_path: Path
    ) -> dict:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as yaml_file:

            return yaml.safe_load(
                yaml_file
            )

    def get_config(self):

        return self.config

    def get_schema(self):

        return self.schema