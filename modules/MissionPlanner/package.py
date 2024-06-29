from pathlib import Path
from pydantic import BaseModel
from modules.module_model import Module, SingleUrlDependency, UrlDependencies


class MissionPlannerParameters(BaseModel):
    installation_path: Path


class MissionPlannerUrlDependencies(UrlDependencies):
    msi: SingleUrlDependency


class MissionPlannerConfigurationFiles(BaseModel):
    config_xml: Path


class MissionPlanner(Module):
    parameters: MissionPlannerParameters
    url_dependencies: MissionPlannerUrlDependencies
    configuration_files: MissionPlannerConfigurationFiles
