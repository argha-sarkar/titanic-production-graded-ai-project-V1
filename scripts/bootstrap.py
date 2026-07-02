from pathlib import Path


PROJECT_DIRECTORIES = [
    "artifacts",
    "configs",
    "data/raw",
    "data/interim",
    "data/processed",
    "data/external",
    "docker",
    "docs",
    "kubernetes",
    "logs",
    "notebooks",
    "requirements",
    "src/api",
    "src/components",
    "src/config",
    "src/constants",
    "src/entity",
    "src/exception",
    "src/logger",
    "src/monitoring",
    "src/pipeline",
    "src/utils",
    "terraform",
    "tests",
]


def create_project_structure() -> None:
    """
    Create all required project directories.
    """

    print("=" * 60)
    print("Creating project structure...")
    print("=" * 60)

    for directory in PROJECT_DIRECTORIES:

        path = Path(directory)

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        print(f"[OK] {path}")

    print("=" * 60)
    print("Project structure is ready.")
    print("=" * 60)


if __name__ == "__main__":

    create_project_structure()