"""GoXLR Utility API: Constants"""

from collections.abc import Callable
from typing import Final

from .models.patch import Patch
from .models.request import Request
from .models.response import Response
from .models.status import Status

# API
KEY_DATA: Final[str] = "data"
KEY_ID: Final[str] = "id"
KEY_TYPE: Final[str] = "type"
REQUEST_TYPE_GET_STATUS: Final[str] = "GetStatus"
RESPONSE_TYPE_PATCH: Final[str] = "Patch"
RESPONSE_TYPE_STATUS: Final[str] = "Status"

# Models
MODEL_PATCH: Final[Callable] = Patch
MODEL_REQUEST: Final[Callable] = Request
MODEL_RESPONSE: Final[Callable] = Response
MODEL_STATUS: Final[Callable] = Status

MODEL_MAP = {
    RESPONSE_TYPE_PATCH: MODEL_PATCH,
    RESPONSE_TYPE_STATUS: MODEL_STATUS,
}
