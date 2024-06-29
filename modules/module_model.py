from pathlib import Path
from typing import Any
from pydantic import BaseModel, field_validator, model_validator


class UrlDependency(BaseModel):
    url: Path
    hash: str


class Module(BaseModel):
    name: str

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
        required_fields = ['configuration_files', 'url_dependencies']
        assert issubclass(
            cls, Module
        ), f"Shoud never get to here, internal pydantic error or missunderstanding the way pydantic works"
        for field in required_fields:
            assert (
                field in cls.model_fields
            ), f"Model {cls} should define the '{field}' field"
        return data
