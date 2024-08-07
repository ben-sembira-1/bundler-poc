import shutil
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Iterable, List, Optional, Tuple, Union
from pydantic import (
    BaseModel,
    field_validator,
    model_validator,
)
from modules.dependencies import SingleFileDependency, SingleUrlDependency


class Module(BaseModel, ABC):
    @property
    def name(self) -> str:
        return self.__class__.__name__
    
    @abstractmethod
    def _collect_all_dependencies(self, dependencies_folder: Path) -> None: ...

    @property
    def subclass_path(self) -> Path:
        subclass__file__ = sys.modules[self.__module__].__file__
        assert isinstance(subclass__file__, str)
        return Path(subclass__file__).parent

    @property
    def dependencies_folder(self) -> Path:
        return self.subclass_path / ".deps"

    def clean_dependencies_folder(self) -> None:
        if self.dependencies_folder.exists():
            print(f"~ Removing {self.dependencies_folder}")
            shutil.rmtree(self.dependencies_folder)

    def pack(self):
        print(f"Packing module {self.name}")
        print("===")
        self.clean_dependencies_folder()
        self.dependencies_folder.mkdir(parents=True)
        self._collect_all_dependencies(self.dependencies_folder)

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

    @model_validator(mode="before")
    @classmethod
    def subclass_defined_required_fields(cls, data: Any) -> Any:
        required_fields = ["configuration_files", "url_dependencies"]
        assert issubclass(
            cls, Module
        ), f"Should never get to here, internal pydantic error or misunderstanding the way pydantic works"
        for field in required_fields:
            assert (
                field in cls.model_fields
            ), f"Model {cls} should define the '{field}' field"
        return data
