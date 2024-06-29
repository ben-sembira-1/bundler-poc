from typing import Union
from modules.Chrome.package import Chrome
from modules.LogsShortcuts.package import LogsShortcuts
from modules.MissionPlanner.package import MissionPlanner
from modules.Neptune.package import Neptune

ModulesAvailable = Union[Chrome, MissionPlanner, Neptune, LogsShortcuts]
