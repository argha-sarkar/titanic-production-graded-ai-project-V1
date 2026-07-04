"""
Project constants.
"""

from pathlib import Path

# ======================================================
# Project Root
# ======================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ======================================================
# Configuration Files
# ======================================================

CONFIG_FILE_PATH = PROJECT_ROOT / "configs" / "config.yaml"

SCHEMA_FILE_PATH = PROJECT_ROOT / "configs" / "schema.yaml"

# ======================================================
# Directories
# ======================================================

DATA_DIR = PROJECT_ROOT / "data"

ARTIFACT_DIR = PROJECT_ROOT / "artifacts"

LOG_DIR = PROJECT_ROOT / "logs"

CONFIG_DIR = PROJECT_ROOT / "configs"

TEST_DIR = PROJECT_ROOT / "tests"

# ======================================================
# Environment
# ======================================================

ENV_FILE = PROJECT_ROOT / ".env"

# ======================================================
# Defaults
# ======================================================

DEFAULT_RANDOM_STATE = 42

DEFAULT_LOG_LEVEL = "INFO"