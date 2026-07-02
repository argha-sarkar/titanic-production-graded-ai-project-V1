from pathlib import Path


REQUIRED_DIRECTORIES = [
    "artifacts",
    "configs",
    "data",
    "src",
    "tests"
]


def test_project_structure():

    for directory in REQUIRED_DIRECTORIES:

        assert Path(directory).exists()