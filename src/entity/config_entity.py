"""
Configuration entities.

This module defines strongly typed configuration
objects used throughout the ML pipeline.
"""

from dataclasses import dataclass
from pathlib import Path


# ==========================================================
# Data Ingestion
# ==========================================================

@dataclass(frozen=True)
class DataIngestionConfig:
    """
    Configuration required for the Data Ingestion component.
    """
    
    root_dir: Path
    
    raw_train_data_path: Path
    
    raw_test_data_path: Path
    
    ingested_train_path: Path

    ingested_test_path: Path
    
# ==========================================================
# Data Validation
# ==========================================================

@dataclass(frozen=True)
class DataValidationConfig:
    """
    Configuration for Data Validation.
    """

    root_dir: Path

    train_file_path: Path

    schema_file_path: Path

    validation_report_file_path: Path

    validation_status_file_path: Path


# ==========================================================
# Data Transformation
# ==========================================================

@dataclass(frozen=True)
class DataTransformationConfig:
    
    """
    Configuration for data transformation.
    """
    
    root_dir: Path

    X_train_path: Path

    y_train_path: Path

    X_test_path: Path

    y_test_path: Path

    preprocessor_path: Path
    
    target_column: str
    
    test_size: float
    
    random_state: int


# ==========================================================
# Model Trainer
# ==========================================================

@dataclass(frozen=True)
class ModelTrainerConfig:

    root_dir: Path

    trained_model_path: Path
    
    
# ==========================================================
# Logging
# ==========================================================

@dataclass(frozen=True)
class LoggingConfig:

    log_level: str

    log_dir: Path
    
    
# ==========================================================
# Data Ingestion Artifact
# ==========================================================

@dataclass(frozen=True)
class DataIngestionArtifact:
    """
    Output of the Data Ingestion component.
    """

    train_file_path: Path

    test_file_path: Path
    
    
# ==========================================================
# Data Validation Artifact
# ==========================================================

@dataclass(frozen=True)
class DataValidationArtifact:
    """
    Output produced by the Data Validation component.
    """

    validation_status: bool

    validated_train_file_path: Path

    report_file_path: Path

    status_file_path: Path
    
    
# ==========================================================
# Data Transformation Artifact
# ==========================================================

@dataclass(frozen=True)
class DataTransformationArtifact:
    X_train_path: Path
    y_train_path: Path
    X_test_path: Path
    y_test_path: Path
    preprocessor_path: Path
    
    