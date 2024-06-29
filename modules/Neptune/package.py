from pathlib import Path
from modules.module_model import Module
from modules.dependencies import SingleUrlDependency, UrlDependencies


class NeptuneUrlDepenecies(UrlDependencies):
    installation_tar: SingleUrlDependency


class Dependencies:
    INSTALLATION_TAR = "neptune_installation.tar"


class Neptune(Module):
    configuration_files: None
    url_dependencies: NeptuneUrlDepenecies

    def _collect_all_dependencies(self, dependecies_folder: Path) -> None:
        self.url_dependencies.installation_tar.pull(
            target=dependecies_folder / Dependencies.INSTALLATION_TAR
        )
