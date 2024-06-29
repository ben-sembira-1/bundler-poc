from pathlib import Path
import json
from typing import Callable, List, Literal, TypeGuard

from pydantic import BaseModel
from modules import ModulesAvailable
from modules.module_model import Module


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
def pack_module(module: Module):
    print(f"Packing module {module.name}")
    print("===")
    module.pack()


def validate_all_dependencies_where_pulled(module: Module):
    LIST_ITEM_PREFIX = "\n  - "
    assert (
        len(module.dependencies_not_pulled) == 0
    ), f"Not all {module.name} dependencies where pulled: [{''.join((LIST_ITEM_PREFIX + str(dep) for dep in module.dependencies_not_pulled))}\n]"


def package_given_entity(entity: Literal["dragonfly", "eagle"]):
    json_raw = Path(f"{entity}_configurations.json").read_text()
    model = BundleConfiguration(**json.loads(json_raw))
    for module in model.modules:
        pack_module(module)
        validate_all_dependencies_where_pulled(module)


def is_valid_entity(entity: str) -> TypeGuard[Entity]:
    return entity in ["eagle", "dragonfly"]


def main():
    import sys

    entity = sys.argv[1]
    assert is_valid_entity(entity), f"{entity} is not a valid entity."
    package_given_entity(entity)


if __name__ == "__main__":
    main()
