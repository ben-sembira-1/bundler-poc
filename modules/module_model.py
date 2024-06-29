import shutil
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Iterable, List, Optional, Tuple, Union
from pydantic import (
    BaseModel,
    HttpUrl,
    GetCoreSchemaHandler,
    PrivateAttr,
    field_validator,
    model_validator,
)
from pydantic_core import CoreSchema, core_schema


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
    _ever_copied: bool = PrivateAttr(default=False)

    def pull(self, target):
        print(f"---")
        print(f"Copying {self.path} to {target}")  # TODO
        self._ever_copied = True

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


class Module(BaseModel, ABC):
    name: str

    @abstractmethod
    def _collect_all_dependencies(self, dependencies_folder: Path) -> None: ...

    @property
    def subclass_path(self) -> Path:
        subclass__file__ = sys.modules[self.__module__].__file__
        assert isinstance(subclass__file__, str)
        return Path(subclass__file__).parent

    @property
    def dependecies_folder(self) -> Path:
        return self.subclass_path / ".deps"

    def clean_dependencies_folder(self) -> None:
        if self.dependecies_folder.exists():
            print(f"~ Removing {self.dependecies_folder}")
            shutil.rmtree(self.dependecies_folder)

    def pack(self):
        self.clean_dependencies_folder()
        self.dependecies_folder.mkdir(parents=True)
        self._collect_all_dependencies(self.dependecies_folder)

    @property
    def _urls_not_pulled(self) -> List[SingleUrlDependency]:
        self.url_dependencies: Optional[
            Iterable[Tuple[str, SingleUrlDependency]]
        ]  # We know that because of the validator at the bottom
        if self.url_dependencies is None:
            return []
        return [dep for _, dep in self.url_dependencies if not dep.ever_pulled]

    @property
    def _configs_not_copied(self) -> List[SingleFileDependency]:
        self.configuration_files: Optional[
            Iterable[Tuple[str, SingleFileDependency]]
        ]  # We know that because of the validator at the bottom
        if self.configuration_files is None:
            return []
        return [
            config for _, config in self.configuration_files if not config.ever_copied
        ]

    @property
    def dependencies_not_pulled(
        self,
    ) -> List[Union[SingleUrlDependency, SingleFileDependency]]:
        return self._urls_not_pulled + self._configs_not_copied

    @field_validator("name")
    @classmethod
    def match_name_to_classname(cls, name: str) -> str:
        currently_validated_module_name = cls.__name__
        assert name == currently_validated_module_name, (
            f"\n\nCould not find module named '{name}'.\n"
            ">>> IMPORTANT: If you recieved this error you can ignore other pydantic errors.\n\n"
        )
        return name

    @model_validator(mode="before")
    @classmethod
    def subclass_defined_requierd_fields(cls, data: Any) -> Any:
        required_fields = ["configuration_files", "url_dependencies"]
        assert issubclass(
            cls, Module
        ), f"Shoud never get to here, internal pydantic error or missunderstanding the way pydantic works"
        for field in required_fields:
            assert (
                field in cls.model_fields
            ), f"Model {cls} should define the '{field}' field"
        return data
