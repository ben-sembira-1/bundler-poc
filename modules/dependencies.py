from pathlib import Path
from typing import Any
from pydantic import (
    BaseModel,
    HttpUrl,
    PrivateAttr,
    field_validator,
)


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
