from pathlib import Path
from pydantic import BaseModel
from modules.module_model import Module, SingleFileDependency, SingleUrlDependency, UrlDependencies


class ChromeParameters(BaseModel):
    dark_mode: bool
    installation_path: Path


class ChromeUrlDependencies(UrlDependencies):
    installer_msi: SingleUrlDependency
    google_translate_addon: SingleUrlDependency


class ChromeConfigurationFiles(BaseModel):
    background_image: SingleFileDependency
    auto_tabs: SingleFileDependency


class Chrome(Module):
    parameters: ChromeParameters
    url_dependencies: ChromeUrlDependencies
    configuration_files: ChromeConfigurationFiles
