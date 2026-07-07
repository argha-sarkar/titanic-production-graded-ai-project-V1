"""
Factory for machine learning models.
"""

from sklearn.ensemble import (
    RandomForestClassifier,
)

from sklearn.linear_model import (
    LogisticRegression,
)

from sklearn.tree import (
    DecisionTreeClassifier,
)

from sklearn.naive_bayes import (
    GaussianNB,
)

from sklearn.neighbors import (
    KNeighborsClassifier,
)


class ModelFactory:
    """
    Create machine learning models.
    """

    @staticmethod
    def get_models():

        return {

            "Logistic Regression":

                LogisticRegression(

                    random_state=42,

                    max_iter=1000,

                ),

            "Decision Tree":

                DecisionTreeClassifier(

                    random_state=42,

                ),

            "Random Forest":

                RandomForestClassifier(

                    random_state=42,

                ),

            "KNN":

                KNeighborsClassifier(),

            "Naive Bayes":

                GaussianNB(),

        }