from logging import config

from src.config.configuration import (
    ConfigurationManager
)


def test_data_ingestion_config():

    manager = ConfigurationManager()

    config = manager.get_data_ingestion_config()

    assert config.raw_train_data_path.name == "train.csv"

    assert config.ingested_train_path.name == "train.csv"


def test_model_trainer_config():

    manager = ConfigurationManager()

    config = manager.get_model_trainer_config()

    assert config.trained_model_path.name == "model.joblib"