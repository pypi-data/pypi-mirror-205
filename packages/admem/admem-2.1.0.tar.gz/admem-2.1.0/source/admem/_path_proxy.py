# Copyright (c) 2022-2023 Mario S. Könz; License: MIT
import os
import typing as tp  # pylint: disable=reimported
from pathlib import _posix_flavour  # type: ignore
from pathlib import _windows_flavour  # type: ignore
from pathlib import Path

from django.core.files.storage import get_storage_class

# 2023-Q1: sphinx has a bug regarding adjusting the signature for attributes,
# hence I need fully qualified imports for typing and django.db

__all__ = ["DjangoPath"]


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
