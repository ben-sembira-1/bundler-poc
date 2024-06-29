from typing import Literal
from pydantic import BaseModel
from modules.module_model import MissionPlanner, Neptune, LogsShortcuts

class DragonflyModules(BaseModel):
    mission_planner: MissionPlanner
    neptune: Neptune
    logs_shortcuts: LogsShortcuts


class DragonflyConfiguration(BaseModel):
    entity: Literal["dragonfly"]
    modules: DragonflyModules