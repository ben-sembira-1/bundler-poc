from typing import Literal
from pydantic import BaseModel
from modules.module_model import Chrome, MissionPlanner, LogsShortcuts

class EagleModules(BaseModel):
    chrome: Chrome
    mission_planner: MissionPlanner
    logs_shortcuts: LogsShortcuts


class EagleConfiguration(BaseModel):
    entity: Literal["eagle"]
    modules: EagleModules