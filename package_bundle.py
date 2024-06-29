from pathlib import Path
import json
from typing import Callable, List, Literal, TypeGuard

from pydantic import BaseModel
from modules import ModulesAvailable


Entity = Literal["eagle", "dragonfly"]


class BundleConfiguration(BaseModel):
    entity: Entity
    modules: List[ModulesAvailable]


def cli_stage_decoration(function: Callable):
    def run_function_with_cli_decoration(*args, **kwargs):
        print("\n----------------------")
        function(*args, **kwargs)
        print("----------------------")

    return run_function_with_cli_decoration


@cli_stage_decoration
def pack_module(module: ModulesAvailable, configuration_files_path: Path):
    print(
        f"Packing module {module.name} using {configuration_files_path}"
    )


def package_given_entity(entity: Literal["dragonfly", "eagle"]):
    json_raw = Path(f"{entity}_configurations.json").read_text()
    model = BundleConfiguration(**json.loads(json_raw))
    configuration_files_path = Path("entities/") / model.entity
    for module in model.modules:
        pack_module(module, configuration_files_path / module.name)


def is_valid_entity(entity: str) -> TypeGuard[Entity]:
    return entity in ['eagle', 'dragonfly']


def main():
    import sys
    entity = sys.argv[1]
    assert is_valid_entity(entity), f"{entity} is not a valid entity."
    package_given_entity(entity)


if __name__ == "__main__":
    main()