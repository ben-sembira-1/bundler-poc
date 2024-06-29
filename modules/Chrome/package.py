from pathlib import Path
from modules.module_model import Module, UrlDependency
from pydantic import BaseModel


class ChromeParameters(BaseModel):
    dark_mode: bool
    installation_path: Path


class ChromeUrlDependencies(BaseModel):
    installer_msi: UrlDependency
    google_translate_addon: UrlDependency


class ChromeConfigurationFiles(BaseModel):
    background_image: Path
    auto_tabs: Path


class Chrome(Module):
    parameters: ChromeParameters
    url_dependencies: ChromeUrlDependencies
    configuration_files: ChromeConfigurationFiles
