import hashlib
from pathlib import Path
import shutil
from typing import Any, Optional
from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    PrivateAttr,
    field_validator,
)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonConfigurationsFolder(metaclass=Singleton):
    def __init__(self, path: Path):
        self._path: Path = path

    @staticmethod
    def instance():
        return SingletonConfigurationsFolder()

    @property
    def path(self) -> Path:
        return self._path


def sha1(file_path: Path) -> str:
    return hashlib.sha1(file_path.read_bytes()).hexdigest()


class SingleUrlDependency(BaseModel):
    url: HttpUrl
    hash: str
    _ever_pulled: bool = PrivateAttr(default=False)

    def pull(self, target: Path):
        print(f"---")
        print(f"Fetching {self.url} to {target}")  # TODO
        self._ever_pulled = True
        print(f"Validating hash of {target}")  # TODO

    @property
    def ever_pulled(self) -> bool:
        return self._ever_pulled


class SingleFileDependency(BaseModel):
    path: Path
    hash: Optional[str] = None
    _configurations_folder: Path
    _ever_copied: bool = PrivateAttr(default=False)

    def pull(self, target: Path):
        print(f"---")
        full_src_path = SingletonConfigurationsFolder.instance().path / self.path
        print(f"Copying {full_src_path} to {target}")
        shutil.copyfile(full_src_path, target)
        self._ever_copied = True
        if self.hash is not None:
            assert sha1(target).startswith(self.hash), (
                f"Hash of {target.as_posix()} starts with {sha1(target)[:len(self.hash)]} "
                f"but {self.hash} is specified in the configuration file."
            )

    @property
    def ever_copied(self) -> bool:
        return self._ever_copied


class UrlDependencies(BaseModel):
    @field_validator("*")
    @classmethod
    def validate_single_url_dependency_type(cls, v: Any) -> SingleUrlDependency:
        assert isinstance(
            v, SingleUrlDependency
        ), f"{v} is not of type SingleUrlDependency"
        return v
