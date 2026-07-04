from src.config.configuration import (
    ConfigurationManager
)

config = ConfigurationManager()

print(config.get_config())

print()

print(config.get_schema())