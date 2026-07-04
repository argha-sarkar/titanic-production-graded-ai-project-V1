from pathlib import Path

import numpy as np

from src.utils.common import (
    save_object,
    load_object,
    save_numpy_array,
    load_numpy_array,
)


def test_joblib():

    obj = {"model": "Titanic"}

    path = Path(
        "artifacts/test_model.joblib"
    )

    save_object(
        path,
        obj
    )

    loaded = load_object(
        path
    )

    assert loaded["model"] == "Titanic"


def test_numpy():

    array = np.array(
        [1, 2, 3]
    )

    path = Path(
        "artifacts/test.npy"
    )

    save_numpy_array(
        path,
        array
    )

    loaded = load_numpy_array(
        path
    )

    assert np.array_equal(
        array,
        loaded
    )