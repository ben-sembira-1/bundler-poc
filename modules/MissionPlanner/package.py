from pathlib import Path
from modules.module_model import Module, UrlDependency
from pydantic import BaseModel


class MissionPlannerParameters(BaseModel):
    installation_path: Path


class MissionPlannerUrlDependencies(BaseModel):
    msi: UrlDependency


class MissionPlannerConfigurationFiles(BaseModel):
    config_xml: Path


class MissionPlanner(Module):
    parameters: MissionPlannerParameters
    url_dependencies: MissionPlannerUrlDependencies
    configuration_files: MissionPlannerConfigurationFiles
