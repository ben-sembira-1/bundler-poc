from pydantic import BaseModel
from modules.module_model import Module, UrlDependency

class NeptuneUrlDepenecies(BaseModel):
    installation_tar: UrlDependency

class Neptune(Module):
    configuration_files: None
    url_dependencies: NeptuneUrlDepenecies

    def package_module(self) -> None:
        pass
