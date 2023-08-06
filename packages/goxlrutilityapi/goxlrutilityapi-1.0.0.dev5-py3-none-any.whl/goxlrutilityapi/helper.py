"""GoXLR Utility API: Helper"""
from __future__ import annotations

from .models.status import Mixer, Status


async def get_mixer_from_status(status: Status) -> Mixer:
    """Get first mixer from status"""
    return next(iter(status.mixers.values()))
