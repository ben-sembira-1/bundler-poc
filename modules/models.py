from pathlib import Path
from typing import List
from pydantic import BaseModel


class Dependency(BaseModel):
    url: Path
    target: str
    hash: str


class Module(BaseModel):
    dependencies: List[Dependency]

    def name(self) -> str:
        return self.__class__.__name__


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


class LogsShortcuts(BaseModel):
    class Parameters(BaseModel):
        log_paths: List[Path]

    parameters: Parameters



