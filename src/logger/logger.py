"""
Production Logger

Provides a single reusable logger for the entire application.
"""

from datetime import datetime
import logging
from pathlib import Path

from src.config.configuration import ConfigurationManager


# ==========================================================
# Load Logging Configuration
# ==========================================================

configuration = ConfigurationManager()

logging_config = configuration.get_logging_config()


# ==========================================================
# Create Log Directory
# ==========================================================

logging_config.log_dir.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================================
# Create Log File
# ==========================================================

current_time = datetime.now().strftime(
    "%Y-%m-%d_%H-%M-%S"
)

log_file = logging_config.log_dir / f"{current_time}.log"


# ==========================================================
# Create Logger
# ==========================================================

logger = logging.getLogger(
    "TitanicProductionML"
)

logger.setLevel(logging_config.log_level)

logger.propagate = False


# ==========================================================
# Formatter
# ==========================================================

formatter = logging.Formatter(

    fmt="%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s",

    datefmt="%Y-%m-%d %H:%M:%S"

)


# ==========================================================
# File Handler
# ==========================================================

file_handler = logging.FileHandler(
    filename=log_file,
    encoding="utf-8"
)

file_handler.setFormatter(formatter)

file_handler.setLevel(logging_config.log_level)


# ==========================================================
# Console Handler
# ==========================================================

console_handler = logging.StreamHandler()

console_handler.setFormatter(formatter)

console_handler.setLevel(logging_config.log_level)


# ==========================================================
# Prevent Duplicate Handlers
# ==========================================================

if not logger.handlers:

    logger.addHandler(file_handler)

    logger.addHandler(console_handler)