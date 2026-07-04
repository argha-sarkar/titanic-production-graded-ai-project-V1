from src.config.configuration import ConfigurationManager
from src.constants import SCHEMA_FILE_PATH
import yaml

def test_load_config():
    config = ConfigurationManager()
    # Access the 'config' attribute directly
    assert config.config is not None

def test_load_schema():
    # Assuming your schema is a YAML file, verify it can be read
    with open(SCHEMA_FILE_PATH, 'r') as f:
        schema = yaml.safe_load(f)
    assert schema is not None