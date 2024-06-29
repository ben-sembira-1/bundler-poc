from pathlib import Path
from typing import Any, List, Union
from pydantic import BaseModel, field_validator, model_validator


class Dependency(BaseModel):
    url: Path
    target: str
    hash: str


class Module(BaseModel):
    name: str
    dependencies: List[Dependency]

    @field_validator('name')
    @classmethod
    def match_name_to_classname(cls, name: str) -> str:
        currently_validated_module_name = cls.__name__
        assert (
            name == currently_validated_module_name
        ), f"Could not find module named '{name}'. If you recieved this error you can ignore other pydantic errors."
        return name

    @model_validator(mode='before')
    @classmethod
    def subclass_defined_configuration_files(cls, data: Any) -> Any:
        REQUIRED_FIELD_NAME = 'configuration_files'
        assert issubclass(
            cls, Module
        ), f"Shoud never get to here, internal pydantic error or missunderstanding the way pydantic works"
        assert (
            REQUIRED_FIELD_NAME in cls.model_fields
        ), f"Model {cls} should define the '{REQUIRED_FIELD_NAME}' field"
        return data


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
    configuration_files: None


class LogsShortcuts(Module):
    class Parameters(BaseModel):
        log_paths: List[Path]

    parameters: Parameters
    configuration_files: None


ModulesAvailable = Union[Chrome, MissionPlanner, Neptune, LogsShortcuts]
