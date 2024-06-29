from pathlib import Path
from pydantic import BaseModel
from modules.module_model import Module
from modules.dependencies import (
    SingleFileDependency,
    SingleUrlDependency,
    UrlDependencies,
)


class MissionPlannerParameters(BaseModel):
    installation_path: Path


class MissionPlannerUrlDependencies(UrlDependencies):
    msi: SingleUrlDependency


class MissionPlannerConfigurationFiles(BaseModel):
    config_xml: SingleFileDependency


class Dependencies:
    MISSION_PLANNER_MSI = "MissionPlanner.msi"
    CONFIG_XML = "config.xml"


class MissionPlanner(Module):
    parameters: MissionPlannerParameters
    url_dependencies: MissionPlannerUrlDependencies
    configuration_files: MissionPlannerConfigurationFiles

    def _collect_all_dependencies(self, dependencies_folder: Path) -> None:
        self.url_dependencies.msi.pull(
            target=dependencies_folder / Dependencies.MISSION_PLANNER_MSI
        )
        self.configuration_files.config_xml.pull(
            target=dependencies_folder / Dependencies.CONFIG_XML
        )
