"""GoXLR Utility API: Response Model"""
from __future__ import annotations

from typing import Any, Optional

from pydantic import Field

from . import DefaultBaseModel


class Response(DefaultBaseModel):
    """Response Model"""

    id: Optional[int] = Field(None, description="Message ID")
    type: Optional[str] = Field(None, description="Type of Response")
    data: Optional[Any] = Field(None, description="Data")
