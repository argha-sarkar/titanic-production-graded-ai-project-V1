from src.models.model_factory import (
    ModelFactory,
)

models = ModelFactory.get_models()

for name in models:

    print(name)