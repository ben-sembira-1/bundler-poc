from pathlib import Path
from typing import Any, List, Literal, Union
from pydantic import BaseModel, model_validator, PydanticUserError


class Dependency(BaseModel):
    url: Path
    target: str
    hash: str


class Module(BaseModel):
    dependencies: List[Dependency]
    configuration_files: None

    @model_validator(mode="before")
    @classmethod
    def subclass_defined_name(cls, data: Any) -> dict:
        assert issubclass(
            cls, Module
        ), f"Shoud never get to here, internal pydantic error or missunderstanding the way pydantic works"
        assert 'name' in cls.model_fields, f"Model {cls} should define the 'name' field"
        return data


# import json
# c = Module(**json.loads("lsdjfk"))
# c.fi


class Chrome(Module):
    class Parameters(BaseModel):
        dark_mode: bool
        installation_path: Path

    class ConfigurationFiles(BaseModel):
        background_image: Path
        auto_tabs: Path

    name: Literal['Chrome']
    parameters: Parameters
    configuration_files: ConfigurationFiles


class MissionPlanner(Module):
    class Parameters(BaseModel):
        installation_path: Path

    class ConfigurationFiles(BaseModel):
        config_xml: Path

    name: Literal["MissionPlanner"]
    parameters: Parameters
    configuration_files: ConfigurationFiles


class Neptune(Module):
    name: Literal["Neptune"]


class LogsShortcuts(Module):
    class Parameters(BaseModel):
        log_paths: List[Path]

    name: Literal["LogsShortcuts"]
    parameters: Parameters


ModulesAvailable = Union[Chrome, MissionPlanner, Neptune, LogsShortcuts]
