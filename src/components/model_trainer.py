"""
Production Model Trainer.
"""
import csv

import json
import sys

import time
from pathlib import Path

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
# Save Artifacts
# ==========================================================

    def _save_results(
        self,
        model,
        leaderboard,
        metrics,
    ):
        """
        Save model and evaluation artifacts.
        """

        create_directories(
            [
                self.config.root_dir,
            ]
        )

        save_object(
            self.config.trained_model_path,
            model,
        )

        with open(
            self.config.metrics_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                metrics,
                file,
                indent=4,
            )

        leaderboard_to_save = []

        for row in leaderboard:

            leaderboard_to_save.append(
                {
                    "model": row["model"],
                    "cv_mean": row["cv_mean"],
                    "cv_std": row["cv_std"],
                }
            )

        pd.DataFrame(
            leaderboard_to_save
        ).to_csv(
            self.config.leaderboard_path,
            index=False,
        )


# ==========================================================
# Main Training Method
# ==========================================================

    def initiate_model_training(
        self,
    ) -> ModelTrainerArtifact:
        """
        Execute the complete model training workflow.
        """

        try:

            logger.info(
                "Starting Model Training."
            )

            (
                X_train,
                y_train,
                X_test,
                y_test,
            ) = self._load_dataset()

            leaderboard = self._evaluate_models(
                X_train,
                y_train,
            )

            start = time.perf_counter()

            model, best = self._train_best_model(
                leaderboard,
                X_train,
                y_train,
            )

            training_time = (
                time.perf_counter() - start
            )

            accuracy, report, matrix = (
                self._evaluate_test_set(
                    model,
                    X_test,
                    y_test,
                )
            )

            model_size = (
                self.config.trained_model_path.stat().st_size
                if self.config.trained_model_path.exists()
                else 0
            )

            metrics = {
                "best_model": best["model"],
                "cv_mean": best["cv_mean"],
                "cv_std": best["cv_std"],
                "test_accuracy": accuracy,
                "training_time_seconds": round(training_time, 4),
                "model_size_kb": round(model_size / 1024, 2),
                "classification_report": report,
                "confusion_matrix": matrix.tolist(),
            }

            self._save_results(
                model,
                leaderboard,
                metrics,
            )
            
            model_size = self.config.trained_model_path.stat().st_size

            logger.info(
                "Model Training Completed."
            )

            return ModelTrainerArtifact(
                best_model_path=self.config.trained_model_path,
                metrics_path=self.config.metrics_path,
                leaderboard_path=self.config.leaderboard_path,
                best_model_name=best["model"],
                best_score=best["cv_mean"],
            )

        except Exception as error:

            logger.exception(
                "Model Training Failed."
            )

            raise CustomException(
                error,
                sys,
            )


# ==========================================================
# Train the Best Candidate
# ==========================================================


# ==========================================================
# Train the Best Candidate
# ==========================================================



# ==========================================================
# Train the Best Candidate
# ==========================================================