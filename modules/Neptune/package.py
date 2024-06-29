from modules.module_model import Module, SingleUrlDependency, UrlDependencies


class NeptuneUrlDepenecies(UrlDependencies):
    installation_tar: SingleUrlDependency


class Neptune(Module):
    configuration_files: None
    url_dependencies: NeptuneUrlDepenecies

    def package_module(self) -> None:
        print(f"Pulling {self.url_dependencies.installation_tar}...")
