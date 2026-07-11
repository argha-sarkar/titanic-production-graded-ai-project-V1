"""
Production Model Trainer.
"""
import csv

import json
import sys

import pandas as pd

from sklearn.ensemble import (
    GradientBoostingClassifier,
    RandomForestClassifier,
)

from sklearn.linear_model import (
    LogisticRegression,
)

from sklearn.model_selection import (
    cross_val_score,
)

from sklearn.tree import (
    DecisionTreeClassifier,
)

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

from src.entity.config_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact,
    ModelTrainerConfig,
)

from src.exception.exception import (
    CustomException,
)

from src.logger.logger import logger

from src.utils.common import (
    load_numpy_array,
    save_object,
    create_directories,
)


class ModelTrainer:
    """
    Train and compare multiple ML models.
    """

    def __init__(
        self,
        config: ModelTrainerConfig,
        transformation_artifact: DataTransformationArtifact,
    ) -> None:

        self.config = config

        self.transformation_artifact = transformation_artifact
    
    
# ==========================================================
# Load Dataset
# ==========================================================   
        
        
    def _load_dataset(
        self,
    ):

        logger.info(
            "Loading transformed datasets."
        )

        X_train = load_numpy_array(
            self.transformation_artifact.X_train_path
        )

        y_train = load_numpy_array(
            self.transformation_artifact.y_train_path
        )

        X_test = load_numpy_array(
            self.transformation_artifact.X_test_path
        )

        y_test = load_numpy_array(
            self.transformation_artifact.y_test_path
        )

        return (

            X_train,

            y_train,

            X_test,

            y_test,

        )
        
        
# ==========================================================
# Create Candidate Models
# ==========================================================

    def _get_models(
        self,
    ):

        return {

            "Logistic Regression":

                LogisticRegression(

                    random_state=self.config.random_state,

                    max_iter=1000,

                ),

            "Decision Tree":

                DecisionTreeClassifier(

                    random_state=self.config.random_state,

                ),

            "Random Forest":

                RandomForestClassifier(

                    random_state=self.config.random_state,

                ),

            "Gradient Boosting":

                GradientBoostingClassifier(

                    random_state=self.config.random_state,

                ),

        }
        
# ==========================================================
# Create Model Evaluation Loop
# ==========================================================

        
    def _evaluate_models(
        self,
        X_train,
        y_train,
    ):
        """
        Perform cross-validation for each candidate model.
        """

        logger.info(
            "Evaluating baseline models."
        )

        leaderboard = []

        models = self._get_models()

        for name, model in models.items():

            scores = cross_val_score(
                estimator=model,
                X=X_train,
                y=y_train,
                cv=self.config.cv_folds,
                scoring=self.config.scoring,
            )

            leaderboard.append(

                {

                    "model": name,

                    "cv_mean": scores.mean(),

                    "cv_std": scores.std(),

                    "estimator": model,

                }

            )

        leaderboard.sort(

            key=lambda row: row["cv_mean"],

            reverse=True,

        )

        return leaderboard

# ==========================================================
# Train the Best Candidate
# ==========================================================

    def _train_best_model(
        self,
        leaderboard,
        X_train,
        y_train,
    ):
        """
        Fit the best candidate on the full training set.
        """

        best = leaderboard[0]

        model = best["estimator"]

        model.fit(
            X_train,
            y_train,
        )

        return model, best
    

# ==========================================================
# Final Test Evaluation
# ==========================================================

    def _evaluate_test_set(
        self,
        model,
        X_test,
        y_test,
    ):
        """
        Evaluate the selected model on the hold-out test set.
        """

        predictions = model.predict(
            X_test
        )

        accuracy = accuracy_score(
            y_test,
            predictions,
        )

        report = classification_report(
            y_test,
            predictions,
        )

        matrix = confusion_matrix(
            y_test,
            predictions,
        )

        return accuracy, report, matrix


# ==========================================================
# Train the Best Candidate
# ==========================================================


# ==========================================================
# Train the Best Candidate
# ==========================================================


# ==========================================================
# Train the Best Candidate
# ==========================================================