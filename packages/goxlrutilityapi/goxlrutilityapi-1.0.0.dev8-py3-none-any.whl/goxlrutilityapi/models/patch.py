"""GoXLR Utility API: Patch Models"""
from __future__ import annotations

from pydantic import Field

from . import DefaultBaseModel


class Patch(DefaultBaseModel):
    """Patch Model"""

    op: str
    path: str
    value: int


class Data(DefaultBaseModel):
    """Data Model"""

    patch: list[Patch] = Field(..., alias="Patch")
