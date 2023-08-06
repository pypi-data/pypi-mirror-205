"""GoXLR Utility API: Patch Models"""
from __future__ import annotations

from typing import Any

from pydantic import Field

from . import DefaultBaseModel


class Patch(DefaultBaseModel):
    """Patch Model"""

    op: str
    path: str
    value: Any


class Data(DefaultBaseModel):
    """Data Model"""

    patch: list[Patch] = Field(..., alias="Patch")
