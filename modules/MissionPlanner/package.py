from pathlib import Path
from pydantic import BaseModel
import shutil
from modules.module_model import (
    Module,
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


MODULE_DEPS_FOLDER = Path(__file__).parent / "deps"


class Dependencies:
    MISSION_PLANNER_MSI = MODULE_DEPS_FOLDER / "MissionPlanner.msi"
    CONFIG_XML = MODULE_DEPS_FOLDER / "config.xml"


class MissionPlanner(Module):
    parameters: MissionPlannerParameters
    url_dependencies: MissionPlannerUrlDependencies
    configuration_files: MissionPlannerConfigurationFiles

    def pack(self) -> None:
        if MODULE_DEPS_FOLDER.exists():
            shutil.rmtree(MODULE_DEPS_FOLDER)
        MODULE_DEPS_FOLDER.mkdir(parents=True)
        self.url_dependencies.msi.pull(target=Dependencies.MISSION_PLANNER_MSI)
        self.configuration_files.config_xml.pull(target=Dependencies.CONFIG_XML)
