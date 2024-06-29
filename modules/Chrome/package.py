from pathlib import Path
from pydantic import BaseModel, field_validator
from modules.module_model import Module
from modules.dependencies import (
    SingleFileDependency,
    SingleUrlDependency,
    UrlDependencies,
)

class ChromeParameters(BaseModel):
    dark_mode: bool
    installation_path: Path


class ChromeUrlDependencies(UrlDependencies):
    installer_msi: SingleUrlDependency
    translate_addon: SingleUrlDependency


class ChromeConfigurationFiles(BaseModel):
    background_image: SingleFileDependency
    auto_tabs: SingleFileDependency

    @field_validator("background_image")
    @classmethod
    def validate_jpeg(cls, background_image: SingleFileDependency) -> SingleFileDependency:
        assert background_image.path.name.endswith(".jpeg"), (
            f"Expecting a jpeg, got {background_image.path.name},"
            " if you want to change it, make sure to change in the dependencies map too"
        )
        return background_image


class Dependencies:
    INSTALLER_MSI = "google-chrome.msi"
    TRANSLATE_ADDON = "google-translate.exe"
    BACKGROUND_JPEG = "background_image.jpeg"
    AUTO_TABS = "background_image.yaml"


class Chrome(Module):
    parameters: ChromeParameters
    url_dependencies: ChromeUrlDependencies
    configuration_files: ChromeConfigurationFiles

    def _collect_all_dependencies(self, dependencies_folder: Path) -> None:
        self.url_dependencies.installer_msi.pull(
            dependencies_folder / Dependencies.INSTALLER_MSI
        )
        self.url_dependencies.translate_addon.pull(
            dependencies_folder / Dependencies.TRANSLATE_ADDON
        )
        self.configuration_files.auto_tabs.pull(
            dependencies_folder / Dependencies.AUTO_TABS
        )
        self.configuration_files.background_image.pull(
            dependencies_folder / Dependencies.BACKGROUND_JPEG
        )
