from pathlib import Path
from typing import List
from modules.module_model import Module
from pydantic import BaseModel


class LogsShortcutsParameters(BaseModel):
    log_paths: List[Path]


class LogsShortcuts(Module):
    parameters: LogsShortcutsParameters
    url_dependencies: None
    configuration_files: None
