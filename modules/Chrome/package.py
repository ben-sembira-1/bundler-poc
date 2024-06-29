from pathlib import Path
from modules.module_model import Module
from pydantic import BaseModel


class ChromeParameters(BaseModel):
    dark_mode: bool
    installation_path: Path


class ChromeConfigurationFiles(BaseModel):
    background_image: Path
    auto_tabs: Path


class Chrome(Module):
    parameters: ChromeParameters
    configuration_files: ChromeConfigurationFiles
