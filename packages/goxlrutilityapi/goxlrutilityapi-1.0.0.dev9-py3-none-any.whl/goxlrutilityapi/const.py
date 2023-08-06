"""GoXLR Utility API: Constants"""

from typing import Any, Final

from .models.patch import Patch
from .models.request import Request
from .models.response import Response
from .models.status import Status

# Connection
DEFAULT_HOST: Final[str] = "localhost"
DEFAULT_PORT: Final[int] = 14564

# Mixer
VOLUME_MAX: Final[int] = 255

# Request/Response Keys
KEY_DATA: Final[str] = "data"
KEY_ID: Final[str] = "id"
KEY_TYPE: Final[str] = "type"

# Request/Response Types
REQUEST_TYPE_GET_STATUS: Final[str] = "GetStatus"
RESPONSE_TYPE_PATCH: Final[str] = "Patch"
RESPONSE_TYPE_STATUS: Final[str] = "Status"

# Models
MODEL_PATCH: type[Patch] = Patch
MODEL_REQUEST: type[Request] = Request
MODEL_RESPONSE: type[Response[Any]] = Response
MODEL_STATUS: type[Status] = Status

MODEL_MAP: Final[dict[str, Any]] = {
    RESPONSE_TYPE_PATCH: MODEL_PATCH,
    RESPONSE_TYPE_STATUS: MODEL_STATUS,
}
