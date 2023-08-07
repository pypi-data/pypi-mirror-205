"""GoXLR Utility API: Map Models"""
from __future__ import annotations

from typing import Optional

from pydantic import Field

from . import DefaultBaseModel


class MapItem(DefaultBaseModel):
    """MapItem Model"""

    name: Optional[str] = Field(None)
    icon: Optional[str] = Field(None)


class Map(DefaultBaseModel):
    """Map Model"""

    __root__: dict[str, MapItem]
