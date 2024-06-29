from pathlib import Path
from pydantic import BaseModel
from modules.module_model import Module, SingleUrlDependency, UrlDependencies


class ChromeParameters(BaseModel):
    dark_mode: bool
    installation_path: Path


class ChromeUrlDependencies(UrlDependencies):
    installer_msi: SingleUrlDependency
    google_translate_addon: SingleUrlDependency


class ChromeConfigurationFiles(BaseModel):
    background_image: Path
    auto_tabs: Path


class Chrome(Module):
    parameters: ChromeParameters
    url_dependencies: ChromeUrlDependencies
    configuration_files: ChromeConfigurationFiles
