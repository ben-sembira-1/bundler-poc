from typing import List
from pathlib import Path
from pydantic import BaseModel
from modules.module_model import Module


class LogsShortcutsParameters(BaseModel):
    log_paths: List[Path]


class LogsShortcuts(Module):
    parameters: LogsShortcutsParameters
    url_dependencies: None
    configuration_files: None
