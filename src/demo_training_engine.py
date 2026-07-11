import numpy as np

from sklearn.linear_model import LogisticRegression

from src.models.trainer import (
    ModelTrainerEngine,
)


X_train = np.array(

    [

        [1, 20],

        [2, 30],

        [3, 40],

        [1, 25],

    ]

)

y_train = np.array(

    [

        0,

        1,

        1,

        0,

    ]

)

X_test = np.array(

    [

        [2, 35],

        [1, 22],

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

print(predictions)