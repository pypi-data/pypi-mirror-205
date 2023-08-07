"""GoXLR Utility API: Status Models"""
from __future__ import annotations

from typing import Any, Optional

from pydantic import Field

from . import DefaultBaseModel


class Config(DefaultBaseModel):
    """Config Model"""

    daemon_version: Optional[str] = Field(None)
    autostart_enabled: Optional[bool] = Field(None)
    show_tray_icon: Optional[bool] = Field(None)
    tts_enabled: Optional[bool] = Field(None)


class Versions(DefaultBaseModel):
    """Versions Model"""

    firmware: Optional[list[int]] = Field(None)
    fpga_count: Optional[int] = Field(None)
    dice: Optional[list[int]] = Field(None)


class UsbDevice(DefaultBaseModel):
    """USB Device Model"""

    manufacturer_name: str
    product_name: str
    version: list[int]
    bus_number: int
    address: int
    identifier: str


class Hardware(DefaultBaseModel):
    """Hardware Model"""

    versions: Versions
    serial_number: str
    manufactured_date: str
    device_type: str
    usb_device: UsbDevice


class FaderStatus(DefaultBaseModel):
    """Fader Status Model"""

    channel: str
    mute_type: str
    scribble: Optional[Any] = Field(None)
    mute_state: str


class FaderStatuses(DefaultBaseModel):
    """Fader Statuses Model"""

    a: FaderStatus = Field(..., alias="A")
    b: FaderStatus = Field(..., alias="B")
    c: FaderStatus = Field(..., alias="C")
    d: FaderStatus = Field(..., alias="D")


class MicGains(DefaultBaseModel):
    """Mic Gains Model"""

    dynamic: Optional[int] = Field(None, alias="Dynamic")
    condenser: Optional[int] = Field(None, alias="Condenser")
    jack: Optional[int] = Field(None, alias="Jack")


class Gain(DefaultBaseModel):
    """Gain Model"""

    equalizer4_k_hz: Optional[int] = Field(None, alias="Equalizer4KHz")
    equalizer16_k_hz: Optional[int] = Field(None, alias="Equalizer16KHz")
    equalizer1_k_hz: Optional[int] = Field(None, alias="Equalizer1KHz")
    equalizer2_k_hz: Optional[int] = Field(None, alias="Equalizer2KHz")
    equalizer125_hz: Optional[int] = Field(None, alias="Equalizer125Hz")
    equalizer500_hz: Optional[int] = Field(None, alias="Equalizer500Hz")
    equalizer31_hz: Optional[int] = Field(None, alias="Equalizer31Hz")
    equalizer63_hz: Optional[int] = Field(None, alias="Equalizer63Hz")
    equalizer8_k_hz: Optional[int] = Field(None, alias="Equalizer8KHz")
    equalizer250_hz: Optional[int] = Field(None, alias="Equalizer250Hz")


class Frequency(DefaultBaseModel):
    """Frequency Model"""

    equalizer16_k_hz: Optional[int] = Field(None, alias="Equalizer16KHz")
    equalizer500_hz: Optional[int] = Field(None, alias="Equalizer500Hz")
    equalizer125_hz: Optional[int] = Field(None, alias="Equalizer125Hz")
    equalizer4_k_hz: Optional[int] = Field(None, alias="Equalizer4KHz")
    equalizer250_hz: Optional[int] = Field(None, alias="Equalizer250Hz")
    equalizer8_k_hz: Optional[int] = Field(None, alias="Equalizer8KHz")
    equalizer2_k_hz: Optional[int] = Field(None, alias="Equalizer2KHz")
    equalizer31_hz: Optional[float] = Field(None, alias="Equalizer31Hz")
    equalizer1_k_hz: Optional[int] = Field(None, alias="Equalizer1KHz")
    equalizer63_hz: Optional[int] = Field(None, alias="Equalizer63Hz")


class Equaliser(DefaultBaseModel):
    """Equaliser Model"""

    gain: Optional[Gain] = Field(None)
    frequency: Optional[Frequency] = Field(None)


class Gain1(DefaultBaseModel):
    """Gain1 Model"""

    equalizer90_hz: Optional[int] = Field(None, alias="Equalizer90Hz")
    equalizer250_hz: Optional[int] = Field(None, alias="Equalizer250Hz")
    equalizer1_k_hz: Optional[int] = Field(None, alias="Equalizer1KHz")
    equalizer3_k_hz: Optional[int] = Field(None, alias="Equalizer3KHz")
    equalizer8_k_hz: Optional[int] = Field(None, alias="Equalizer8KHz")
    equalizer500_hz: Optional[int] = Field(None, alias="Equalizer500Hz")


class Frequency1(DefaultBaseModel):
    """Frequency1 Model"""

    equalizer3_k_hz: Optional[int] = Field(None, alias="Equalizer3KHz")
    equalizer1_k_hz: Optional[int] = Field(None, alias="Equalizer1KHz")
    equalizer90_hz: Optional[int] = Field(None, alias="Equalizer90Hz")
    equalizer250_hz: Optional[int] = Field(None, alias="Equalizer250Hz")
    equalizer8_k_hz: Optional[int] = Field(None, alias="Equalizer8KHz")
    equalizer500_hz: Optional[int] = Field(None, alias="Equalizer500Hz")


class EqualiserMini(DefaultBaseModel):
    """Equaliser Mini Model"""

    gain: Optional[Gain1] = Field(None)
    frequency: Optional[Frequency1] = Field(None)


class NoiseGate(DefaultBaseModel):
    """Noise Gate Model"""

    threshold: Optional[int] = Field(None)
    attack: Optional[int] = Field(None)
    release: Optional[int] = Field(None)
    enabled: Optional[bool] = Field(None)
    attenuation: Optional[int] = Field(None)


class Compressor(DefaultBaseModel):
    """Compressor Model"""

    threshold: Optional[int] = Field(None)
    ratio: Optional[int] = Field(None)
    attack: Optional[int] = Field(None)
    release: Optional[int] = Field(None)
    makeup_gain: Optional[int] = Field(None)


class MicStatus(DefaultBaseModel):
    """Mic Status Model"""

    mic_type: Optional[str] = Field(None)
    mic_gains: Optional[MicGains] = Field(None)
    equaliser: Optional[Equaliser] = Field(None)
    equaliser_mini: Optional[EqualiserMini] = Field(None)
    noise_gate: Optional[NoiseGate] = Field(None)
    compressor: Optional[Compressor] = Field(None)


class Volumes(DefaultBaseModel):
    """Volumes Model"""

    mic: int = Field(..., alias="Mic")
    line_in: int = Field(..., alias="LineIn")
    console: int = Field(..., alias="Console")
    system: int = Field(..., alias="System")
    game: int = Field(..., alias="Game")
    chat: int = Field(..., alias="Chat")
    sample: int = Field(..., alias="Sample")
    music: int = Field(..., alias="Music")
    headphones: int = Field(..., alias="Headphones")
    mic_monitor: int = Field(..., alias="MicMonitor")
    line_out: int = Field(..., alias="LineOut")


class Levels(DefaultBaseModel):
    """Levels Model"""

    submix_supported: Optional[bool] = Field(None)
    volumes: Volumes
    submix: Optional[Any] = Field(None)
    bleep: Optional[int] = Field(None)
    deess: Optional[int] = Field(None)


class RouterItem(DefaultBaseModel):
    """Router Item Model"""

    headphones: Optional[bool] = Field(None, alias="Headphones")
    broadcast_mix: Optional[bool] = Field(None, alias="BroadcastMix")
    chat_mic: Optional[bool] = Field(None, alias="ChatMic")
    sampler: Optional[bool] = Field(None, alias="Sampler")
    line_out: Optional[bool] = Field(None, alias="LineOut")


class Router(DefaultBaseModel):
    """Router Model"""

    microphone: Optional[RouterItem] = Field(None, alias="Microphone")
    chat: Optional[RouterItem] = Field(None, alias="Chat")
    music: Optional[RouterItem] = Field(None, alias="Music")
    game: Optional[RouterItem] = Field(None, alias="Game")
    console: Optional[RouterItem] = Field(None, alias="Console")
    line_in: Optional[RouterItem] = Field(None, alias="LineIn")
    system: Optional[RouterItem] = Field(None, alias="System")
    samples: Optional[RouterItem] = Field(None, alias="Samples")


class CoughButton(DefaultBaseModel):
    """Cough Button Model"""

    is_toggle: Optional[bool] = Field(None)
    mute_type: Optional[str] = Field(None)
    state: Optional[str] = Field(None)


class Colours(DefaultBaseModel):
    """Colours Model"""

    colour_one: Optional[str] = Field(None)
    colour_two: Optional[str] = Field(None)


class Fader(DefaultBaseModel):
    """Fader Model"""

    style: Optional[str] = Field(None)
    colours: Colours = Field(None)


class Faders(DefaultBaseModel):
    """Faders Model"""

    a: Fader = Field(..., alias="A")
    b: Fader = Field(..., alias="B")
    c: Fader = Field(..., alias="C")
    d: Fader = Field(..., alias="D")


class Button(DefaultBaseModel):
    """Button Model"""

    off_style: Optional[str]
    colours: Colours


class Buttons(DefaultBaseModel):
    """Buttons Model"""

    bleep: Button = Field(..., alias="Bleep")
    cough: Button = Field(..., alias="Cough")
    fader1_mute: Button = Field(..., alias="Fader1Mute")
    fader2_mute: Button = Field(..., alias="Fader2Mute")
    fader3_mute: Button = Field(..., alias="Fader3Mute")
    fader4_mute: Button = Field(..., alias="Fader4Mute")


class Global(DefaultBaseModel):
    """Global Model"""

    colour_one: Optional[str]


class Accent(DefaultBaseModel):
    """Accent Model"""

    colour_one: Optional[str]


class Simple(DefaultBaseModel):
    """Simple Model"""

    global_: Optional[Global] = Field(None, alias="Global")
    accent: Accent = Field(None, alias="Accent")


class Lighting(DefaultBaseModel):
    """Lighting Model"""

    faders: Faders
    buttons: Buttons
    simple: Simple
    sampler: Optional[dict[str, Any]]
    encoders: Optional[dict[str, Any]]


class Display(DefaultBaseModel):
    """Display Model"""

    gate: Optional[str]
    compressor: Optional[str]
    equaliser: Optional[str]
    equaliser_fine: Optional[str]


class Settings(DefaultBaseModel):
    """Settings Model"""

    display: Optional[Display]
    mute_hold_duration: Optional[int]
    vc_mute_also_mute_cm: Optional[bool]


class ButtonDown(DefaultBaseModel):
    """Button Down Model"""

    bleep: Optional[bool] = Field(None, alias="Bleep")
    cough: Optional[bool] = Field(None, alias="Cough")
    effect_fx: Optional[bool] = Field(None, alias="EffectFx")
    effect_hard_tune: Optional[bool] = Field(None, alias="EffectHardTune")
    effect_megaphone: Optional[bool] = Field(None, alias="EffectMegaphone")
    effect_robot: Optional[bool] = Field(None, alias="EffectRobot")
    effect_select1: Optional[bool] = Field(None, alias="EffectSelect1")
    effect_select2: Optional[bool] = Field(None, alias="EffectSelect2")
    effect_select3: Optional[bool] = Field(None, alias="EffectSelect3")
    effect_select4: Optional[bool] = Field(None, alias="EffectSelect4")
    effect_select5: Optional[bool] = Field(None, alias="EffectSelect5")
    effect_select6: Optional[bool] = Field(None, alias="EffectSelect6")
    fader1_mute: Optional[bool] = Field(None, alias="Fader1Mute")
    fader2_mute: Optional[bool] = Field(None, alias="Fader2Mute")
    fader3_mute: Optional[bool] = Field(None, alias="Fader3Mute")
    fader4_mute: Optional[bool] = Field(None, alias="Fader4Mute")
    sampler_bottom_left: Optional[bool] = Field(None, alias="SamplerBottomLeft")
    sampler_bottom_right: Optional[bool] = Field(None, alias="SamplerBottomRight")
    sampler_clear: Optional[bool] = Field(None, alias="SamplerClear")
    sampler_select_a: Optional[bool] = Field(None, alias="SamplerSelectA")
    sampler_select_b: Optional[bool] = Field(None, alias="SamplerSelectB")
    sampler_select_c: Optional[bool] = Field(None, alias="SamplerSelectC")
    sampler_top_left: Optional[bool] = Field(None, alias="SamplerTopLeft")
    sampler_top_right: Optional[bool] = Field(None, alias="SamplerTopRight")


class Mixer(DefaultBaseModel):
    """Mixer Model"""

    hardware: Hardware
    shutdown_commands: list
    fader_status: FaderStatuses
    mic_status: MicStatus
    levels: Levels
    router: Router
    cough_button: CoughButton
    lighting: Lighting
    effects: Any
    sampler: Any
    settings: Settings
    button_down: ButtonDown
    profile_name: str
    mic_profile_name: str


class Paths(DefaultBaseModel):
    """Paths Model"""

    profile_directory: Optional[str]
    mic_profile_directory: Optional[str]
    samples_directory: Optional[str]
    presets_directory: Optional[str]
    icons_directory: Optional[str]


class Files(DefaultBaseModel):
    """Files Model"""

    profiles: Optional[list[str]]
    mic_profiles: Optional[list[str]]
    presets: Optional[list[str]]
    samples: Optional[dict[str, Any]]
    icons: Optional[list[str]]


class Status(DefaultBaseModel):
    """Status Model"""

    config: Config
    mixers: dict[str, Mixer]
    paths: Paths
    files: Files


class Data(DefaultBaseModel):
    """Data Model"""

    status: Status = Field(..., alias="Status")
