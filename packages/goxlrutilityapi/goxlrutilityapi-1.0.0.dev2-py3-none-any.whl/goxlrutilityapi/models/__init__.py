"""GoXLR Utility API: Models"""

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class DefaultBaseModel(BaseModel):
    """Default Base Model"""

    class Config:  # pylint: disable=missing-class-docstring
        extra = "allow"
