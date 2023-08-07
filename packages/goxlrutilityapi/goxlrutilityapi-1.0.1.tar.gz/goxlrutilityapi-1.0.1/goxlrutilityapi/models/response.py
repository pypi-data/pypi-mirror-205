"""GoXLR Utility API: Response Model"""
from __future__ import annotations

from typing import Generic, Optional, TypeVar

from pydantic import Field

from . import DefaultBaseModel

T = TypeVar("T")


class Response(DefaultBaseModel, Generic[T]):
    """Response Model"""

    id: Optional[int] = Field(None, description="Message ID")
    type: Optional[str] = Field(None, description="Type of Response")
    data: T = Field(None, description="Data")
