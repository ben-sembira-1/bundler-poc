from typing import Literal
from pydantic import BaseModel
from modules.models import Chrome, MissionPlanner, LogsShortcuts

class EagleModules(BaseModel):
    chrome: Chrome
    mission_planner: MissionPlanner
    logs_shortcuts: LogsShortcuts


class EagleConfiguration(BaseModel):
    entity: Literal["eagle"]
    modules: EagleModules