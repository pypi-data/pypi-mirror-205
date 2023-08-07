"""GoXLR Utility API: Map Model"""
from __future__ import annotations

from typing import Optional

from pydantic import Field

from . import DefaultBaseModel


class MapItem(DefaultBaseModel):
    """MapItem Model"""

    name: Optional[str] = Field(None)
    icon: Optional[str] = Field(None)
