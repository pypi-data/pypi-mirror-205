# Copyright (c) 2022-2023 Mario S. Könz; License: MIT
import os
import typing as tp  # pylint: disable=reimported
from pathlib import _posix_flavour  # type: ignore
from pathlib import _windows_flavour  # type: ignore
from pathlib import Path

from django.core.files.storage import get_storage_class
from django.db import models

# 2023-Q1: sphinx has a bug regarding adjusting the signature for attributes,
# hence I need fully qualified imports for typing and django.db

__all__ = ["DjangoPath", "DjangoPathField"]


class DjangoPath(Path):
    _flavour = _windows_flavour if os.name == "nt" else _posix_flavour

    def open(  # type: ignore  # pylint: disable=too-many-arguments
        self,
        mode: str = "r",
        buffering: int = -1,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
    ) -> tp.IO[tp.Any]:
        # assert encoding is None
        assert errors is None
        assert newline is None
        assert buffering == -1
        media_storage = get_storage_class()()
        return media_storage.open(self.as_posix(), mode=mode)


class DjangoPathField(models.Field):  # type: ignore
    def __init__(
        self, *args: tp.Any, upload_to: str | None = None, **kwgs: tp.Any
    ) -> None:
        self.upload_to = upload_to
        super().__init__(*args, **kwgs)

    def db_type(self, connection: tp.Any) -> str:
        return f"char({self.max_length})"

    def deconstruct(self) -> tp.Any:
        name, path, args, kwargs = super().deconstruct()
        # Only include kwarg if it's not the default
        if self.max_length != 1024:
            kwargs["max_length"] = self.max_length
        if self.upload_to is not None:
            kwargs["upload_to"] = self.upload_to
        return name, path, args, kwargs

    def from_db_value(  # pylint: disable=unused-argument
        self,
        value: str,
        expression: str,
        connection: tp.Any,
    ) -> DjangoPath:
        if value is None:
            return value
        return DjangoPath(value)

    def to_python(self, value: DjangoPath | str | None) -> DjangoPath | None:
        if isinstance(value, DjangoPath):
            return value

        if value is None:
            return value

        return DjangoPath(value)

    def pre_save(self, model_instance: tp.Any, add: bool = True) -> DjangoPath | None:
        path = super().pre_save(model_instance, add=add)
        name = self.get_name(path)
        storage = get_storage_class()()
        if name and not storage.exists(name):
            with path.open("rb") as f:
                storage.save(name, f)
            djpath = DjangoPath(name)
        else:
            djpath = None
        setattr(model_instance, self.name, djpath)
        return djpath

    def get_prep_value(self, value: DjangoPath) -> str | None:
        if value is None:
            return value
        return value.as_posix()

    def get_name(self, value: Path | None) -> str | None:
        if value is None:
            return value
        if isinstance(self.upload_to, str):
            return (Path(self.upload_to) / value.name).as_posix()
        if self.upload_to is None:
            return value.name
        raise NotImplementedError(self.upload_to)
