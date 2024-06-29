from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Iterable, Optional, Tuple
from pydantic import BaseModel, PrivateAttr, field_validator, model_validator


class SingleUrlDependency(BaseModel):
    url: Path
    hash: str
    _ever_pulled: bool = PrivateAttr(default=False)

    def pull(self, target_directory: Path, target_file_name: Optional[str] = None):
        self._ever_pulled = True
        target_file_name = (
            self.url.name if target_file_name is None else target_file_name
        )
        target_path = target_directory / target_file_name
        print(f"Pulling {self.url} to {target_path}...")  # TODO
        print(f"Validating hash of {target_path}...")  # TODO

    @property
    def ever_pulled(self) -> bool:
        return self._ever_pulled


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

    # @abstractmethod
    # def package_module(self) -> None: ...

    @property
    def all_url_dependencies_where_pulled(self) -> bool:
        self.url_dependencies: Iterable[Tuple[str, SingleUrlDependency]]  # We now that because of the validator at the bottom
        return all(
            dep.ever_pulled for _, dep in self.url_dependencies
        )

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
