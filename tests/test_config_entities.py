from src.config.configuration import (
    ConfigurationManager
)


def test_data_ingestion_config():

    manager = ConfigurationManager()

    config = manager.get_data_ingestion_config()

    assert config.train_file_path.name == "train.csv"


def test_model_trainer_config():

    manager = ConfigurationManager()

    config = manager.get_model_trainer_config()

    assert config.trained_model_path.name == "model.joblib"