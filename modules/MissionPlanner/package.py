from pathlib import Path
from modules.module_model import Module
from pydantic import BaseModel


class MissionPlannerParameters(BaseModel):
    installation_path: Path


class MissionPlannerConfigurationFiles(BaseModel):
    config_xml: Path


class MissionPlanner(Module):
    parameters: MissionPlannerParameters
    configuration_files: MissionPlannerConfigurationFiles
