"""GoXLR Utility API: Helper"""
from __future__ import annotations

from typing import Optional

from .const import VOLUME_MAX
from .models.status import Mixer, Status


def get_mixer_from_status(status: Status) -> Optional[Mixer]:
    """Get first mixer from status"""
    return next(iter(status.mixers.values()), None)


def get_volume_percentage(
    mixer: Mixer,
    key: str,
) -> Optional[int]:
    """Return the volume in percent."""
    if (value := getattr(mixer.levels.volumes, key, None)) is not None:
        return round(value / VOLUME_MAX * 100)
    return None
