from pathlib import Path
import json
from typing import List, Literal

from pydantic import BaseModel
from modules.models import ModulesAvailable


class BundleConfiguration(BaseModel):
    entity: Literal["eagle", "dragonfly"]
    modules: List[ModulesAvailable]


def main(entity: Literal['dragonfly', 'eagle']):
    json_raw = Path(f"{entity}_configurations.json").read_text()
    model = BundleConfiguration(**json.loads(json_raw))
    print(model)
    print("----------------------")
    print(model.modules)
    print("----------------------")
    configuration_files_path = Path("entities/") / model.entity
    print(configuration_files_path)
    print("----------------------")
    # for module in model.modules:
    #     print(f"==={module.name}===")
    #     print(f"{module.configuration_files}")
    #     breakpoint()
    print("----------------------")
    print("----------------------")
    print("----------------------")


if __name__ == "__main__":
    main('dragonfly')
