"""GoXLR Utility API: Request Model"""
from __future__ import annotations

from typing import Optional

from pydantic import Field

from . import DefaultBaseModel


class Request(DefaultBaseModel):
    """Request Model"""

    id: Optional[int] = None
    data: str = Field(..., description="Data")
