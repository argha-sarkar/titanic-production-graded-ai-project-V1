import numpy as np

from sklearn.linear_model import (
    LogisticRegression,
)

from src.models.trainer import (
    ModelTrainerEngine,
)


def test_training_engine():

    X_train = np.array(

        [

            [1, 10],

            [2, 20],

            [3, 30],

            [4, 40],

        ]

    )

    y_train = np.array(

        [

            0,

            0,

            1,

            1,

        ]

    )

    X_test = np.array(

        [

            [2, 15],

            [3, 35],

        ]

    )

    model = LogisticRegression()

    trained_model, predictions = (

        ModelTrainerEngine.train(

            model,

            X_train,

            y_train,

            X_test,

        )

    )

    assert len(predictions) == 2