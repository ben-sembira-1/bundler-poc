from pathlib import Path
from typing import List, Union
from pydantic import BaseModel, field_validator


class Dependency(BaseModel):
    url: Path
    target: str
    hash: str


class Module(BaseModel):
    name: str
    dependencies: List[Dependency]
    configuration_files: None

    @field_validator('name')
    @classmethod
    def name_matches_classname(cls, name: str) -> str:
        currently_validated_module_name = cls.__name__
        assert (
            name == currently_validated_module_name
        ), f"Could not find module named '{name}'. If you recieved this error you can ignore other pydantic errors."
        return name


class Chrome(Module):
    class Parameters(BaseModel):
        dark_mode: bool
        installation_path: Path

    class ConfigurationFiles(BaseModel):
        background_image: Path
        auto_tabs: Path

    parameters: Parameters
    configuration_files: ConfigurationFiles


class MissionPlanner(Module):
    class Parameters(BaseModel):
        installation_path: Path

    class ConfigurationFiles(BaseModel):
        config_xml: Path

    parameters: Parameters
    configuration_files: ConfigurationFiles


class Neptune(Module):
    pass


class LogsShortcuts(Module):
    class Parameters(BaseModel):
        log_paths: List[Path]

    parameters: Parameters


ModulesAvailable = Union[Chrome, MissionPlanner, Neptune, LogsShortcuts]
