"""
Common utility functions for the project.
"""

from pathlib import Path
from typing import Any

import joblib
import numpy as np
import yaml

from src.logger.logger import logger
from src.exception.exception import CustomException

import sys


# ==========================================================
# YAML
# ==========================================================

def read_yaml(file_path: Path) -> dict:
    """
    Read a YAML file.
    """

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as yaml_file:

            return yaml.safe_load(yaml_file)

    except Exception as error:

        logger.exception(
            "Unable to read YAML."
        )

        raise CustomException(
            error,
            sys
        )


def write_yaml(
    file_path: Path,
    content: dict
) -> None:
    """
    Write a dictionary into a YAML file.
    """

    try:

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as yaml_file:

            yaml.safe_dump(
                content,
                yaml_file,
                sort_keys=False
            )

    except Exception as error:

        logger.exception(
            "Unable to write YAML."
        )

        raise CustomException(
            error,
            sys
        )


# ==========================================================
# Directory
# ==========================================================

def create_directories(
    directories: list[Path]
) -> None:
    """
    Create multiple directories.
    """

    try:

        for directory in directories:

            directory.mkdir(
                parents=True,
                exist_ok=True
            )

    except Exception as error:

        logger.exception(
            "Directory creation failed."
        )

        raise CustomException(
            error,
            sys
        )


# ==========================================================
# Joblib
# ==========================================================

def save_object(
    file_path: Path,
    obj: Any
) -> None:
    """
    Save a Python object.
    """

    try:

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        joblib.dump(
            obj,
            file_path
        )

    except Exception as error:

        logger.exception(
            "Object saving failed."
        )

        raise CustomException(
            error,
            sys
        )


def load_object(
    file_path: Path
) -> Any:
    """
    Load a Python object.
    """

    try:

        return joblib.load(
            file_path
        )

    except Exception as error:

        logger.exception(
            "Object loading failed."
        )

        raise CustomException(
            error,
            sys
        )


# ==========================================================
# NumPy
# ==========================================================

def save_numpy_array(
    file_path: Path,
    array: np.ndarray
) -> None:
    """
    Save NumPy array.
    """

    try:

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        np.save(
            file_path,
            array
        )

    except Exception as error:

        logger.exception(
            "Saving NumPy array failed."
        )

        raise CustomException(
            error,
            sys
        )


def load_numpy_array(
    file_path: Path
) -> np.ndarray:
    """
    Load NumPy array.
    """

    try:

        return np.load(
            file_path
        )

    except Exception as error:

        logger.exception(
            "Loading NumPy array failed."
        )

        raise CustomException(
            error,
            sys
        )