from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Iterable, Optional, Tuple
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
    def pack(self) -> None: ...

    @property
    def _all_urls_where_pulled(self) -> bool:
        self.url_dependencies: Optional[
            Iterable[Tuple[str, SingleUrlDependency]]
        ]  # We know that because of the validator at the bottom
        if self.url_dependencies is None:
            return True
        return all(dep.ever_pulled for _, dep in self.url_dependencies)

    @property
    def _all_configs_where_copied(self) -> bool:
        self.configuration_files: Optional[
            Iterable[Tuple[str, SingleFileDependency]]
        ]  # We know that because of the validator at the bottom
        if self.configuration_files is None:
            return True
        return all(config.ever_copied for _, config in self.configuration_files)

    @property
    def all_dependencies_where_pulled(self) -> bool:
        return self._all_urls_where_pulled and self._all_configs_where_copied

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
