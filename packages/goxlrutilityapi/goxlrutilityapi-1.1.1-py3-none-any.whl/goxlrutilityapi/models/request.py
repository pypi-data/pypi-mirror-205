"""GoXLR Utility API: Request Model"""
from __future__ import annotations

from typing import Any, Optional, Union

from pydantic import Field

from . import DefaultBaseModel


class Request(DefaultBaseModel):
    """Request Model"""

    id: Optional[int] = None
    data: Union[str, dict[str, Any]] = Field(..., description="Data")
