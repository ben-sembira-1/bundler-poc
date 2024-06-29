from pathlib import Path
import shutil
from modules.module_model import Module, SingleUrlDependency, UrlDependencies


class NeptuneUrlDepenecies(UrlDependencies):
    installation_tar: SingleUrlDependency


MODULE_DEPS_FOLDER = Path(__file__).parent / "deps"


class Dependencies:
    INSTALLATION_TAR = MODULE_DEPS_FOLDER / "neptune_installation.tar"


class Neptune(Module):
    configuration_files: None
    url_dependencies: NeptuneUrlDepenecies

    def pack(self) -> None:
        if MODULE_DEPS_FOLDER.exists():
            shutil.rmtree(MODULE_DEPS_FOLDER)
        MODULE_DEPS_FOLDER.mkdir(parents=True)
        self.url_dependencies.installation_tar.pull(
            target=Dependencies.INSTALLATION_TAR
        )
