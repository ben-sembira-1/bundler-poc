from pathlib import Path
import json
from typing import Union, Literal, TypeGuard

from pydantic import BaseModel
from modules import Chrome, MissionPlanner, LogsShortcuts, Neptune
from modules.dependencies import SingletonConfigurationsFolder
from modules.module import Module


Entity = Literal["eagle", "dragonfly"]


class EagleModules(BaseModel):
  chrome: Chrome
  mission_planner: MissionPlanner
  logs_shortcuts: LogsShortcuts


class DragonflyModules(BaseModel):
  neptune: Neptune
  mission_planner: MissionPlanner
  logs_shortcuts: LogsShortcuts


class BundleConfiguration(BaseModel):
    entity: Entity
    modules: Union[EagleModules, DragonflyModules]


def validate_all_dependencies_where_pulled(module: Module):
    LIST_ITEM_PREFIX = "\n  - "
    assert (
        len(module.dependencies_not_pulled) == 0
    ), f"Not all {module.name} dependencies where pulled: [{''.join((LIST_ITEM_PREFIX + str(dep) for dep in module.dependencies_not_pulled))}\n]"


def pack_module(module: Module):
    print("\n----------------------")
    module.pack()
    validate_all_dependencies_where_pulled(module)
    print("----------------------")


def load_bundle_from_json(json_path: Path) -> BundleConfiguration:
    json_raw = json_path.read_text()
    return BundleConfiguration(**json.loads(json_raw))


def pack_all(entity: Literal["dragonfly", "eagle"]):
    bundle = load_bundle_from_json(Path(f"{entity}_configurations.json"))
    for _, module in bundle.modules:
        pack_module(module)


def is_valid_entity(entity: str) -> TypeGuard[Entity]:
    return entity in ["eagle", "dragonfly"]


def main():
    import os
    import sys

    assert (
        Path(os.getcwd()) == Path(__file__).parent
    ), "Please run the script from the folder it is located in."

    entity = sys.argv[1]
    assert is_valid_entity(entity), f"{entity} is not a valid entity."
    SingletonConfigurationsFolder(path=Path(os.getcwd()) / "entities" / entity)
    pack_all(entity)


if __name__ == "__main__":
    main()
