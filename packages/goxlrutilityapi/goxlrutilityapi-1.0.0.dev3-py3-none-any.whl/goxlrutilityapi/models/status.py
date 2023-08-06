"""GoXLR Utility API: Status Models"""
from __future__ import annotations

from typing import Any, Optional

from pydantic import Field

from . import DefaultBaseModel


class Config(DefaultBaseModel):
    """Config Model"""

    daemon_version: Optional[str] = Field(None, alias="DaemonVersion")
    autostart_enabled: Optional[bool] = Field(None, alias="AutostartEnabled")
    show_tray_icon: Optional[bool] = Field(None, alias="ShowTrayIcon")
    tts_enabled: Optional[bool] = Field(None, alias="TTSEnabled")


class Versions(DefaultBaseModel):
    """Versions Model"""

    firmware: Optional[list[int]] = Field(None, alias="Firmware")
    fpga_count: Optional[int] = Field(None, alias="FPGACount")
    dice: Optional[list[int]] = Field(None, alias="DICE")


class UsbDevice(DefaultBaseModel):
    """USB Device Model"""

    manufacturer_name: Optional[str] = Field(None, alias="ManufacturerName")
    product_name: Optional[str] = Field(None, alias="ProductName")
    version: Optional[list[int]] = Field(None, alias="Version")
    bus_number: Optional[int] = Field(None, alias="BusNumber")
    address: Optional[int] = Field(None, alias="Address")
    identifier: Optional[str] = Field(None, alias="Identifier")


class Hardware(DefaultBaseModel):
    """Hardware Model"""

    versions: Optional[Versions] = Field(None, alias="Versions")
    serial_number: Optional[str] = Field(None, alias="SerialNumber")
    manufactured_date: Optional[str] = Field(None, alias="ManufacturedDate")
    device_type: Optional[str] = Field(None, alias="DeviceType")
    usb_device: Optional[UsbDevice] = Field(None, alias="USBDevice")


class FaderStatus(DefaultBaseModel):
    """Fader Status Model"""

    channel: Optional[str] = Field(None, alias="Channel")
    mute_type: Optional[str] = Field(None, alias="MuteType")
    scribble: Optional[Any] = Field(None, alias="Scribble")
    mute_state: Optional[str] = Field(None, alias="MuteState")


class FaderStatuses(DefaultBaseModel):
    """Fader Statuses Model"""

    a: Optional[FaderStatus] = Field(None, alias="A")
    b: Optional[FaderStatus] = Field(None, alias="B")
    c: Optional[FaderStatus] = Field(None, alias="C")
    d: Optional[FaderStatus] = Field(None, alias="D")


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

    gain: Optional[Gain] = Field(None, alias="Gain")
    frequency: Optional[Frequency] = Field(None, alias="Frequency")


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

    gain: Optional[Gain1] = Field(None, alias="Gain")
    frequency: Optional[Frequency1] = Field(None, alias="Frequency")


class NoiseGate(DefaultBaseModel):
    """Noise Gate Model"""

    threshold: Optional[int] = Field(None, alias="Threshold")
    attack: Optional[int] = Field(None, alias="Attack")
    release: Optional[int] = Field(None, alias="Release")
    enabled: Optional[bool] = Field(None, alias="Enabled")
    attenuation: Optional[int] = Field(None, alias="Attenuation")


class Compressor(DefaultBaseModel):
    """Compressor Model"""

    threshold: Optional[int] = Field(None, alias="Threshold")
    ratio: Optional[int] = Field(None, alias="Ratio")
    attack: Optional[int] = Field(None, alias="Attack")
    release: Optional[int] = Field(None, alias="Release")
    makeup_gain: Optional[int] = Field(None, alias="MakeupGain")


class MicStatus(DefaultBaseModel):
    """Mic Status Model"""

    mic_type: Optional[str] = Field(None, alias="MicType")
    mic_gains: Optional[MicGains] = Field(None, alias="MicGains")
    equaliser: Optional[Equaliser] = Field(None, alias="Equaliser")
    equaliser_mini: Optional[EqualiserMini] = Field(None, alias="EqualiserMini")
    noise_gate: Optional[NoiseGate] = Field(None, alias="NoiseGate")
    compressor: Optional[Compressor] = Field(None, alias="Compressor")


class Volumes(DefaultBaseModel):
    """Volumes Model"""

    mic: Optional[int] = Field(None, alias="Mic")
    line_in: Optional[int] = Field(None, alias="LineIn")
    console: Optional[int] = Field(None, alias="Console")
    system: Optional[int] = Field(None, alias="System")
    game: Optional[int] = Field(None, alias="Game")
    chat: Optional[int] = Field(None, alias="Chat")
    sample: Optional[int] = Field(None, alias="Sample")
    music: Optional[int] = Field(None, alias="Music")
    headphones: Optional[int] = Field(None, alias="Headphones")
    mic_monitor: Optional[int] = Field(None, alias="MicMonitor")
    line_out: Optional[int] = Field(None, alias="LineOut")


class Levels(DefaultBaseModel):
    """Levels Model"""

    submix_supported: Optional[bool] = Field(None, alias="SubmixSupported")
    volumes: Optional[Volumes] = Field(None, alias="Volumes")
    submix: Optional[Any] = Field(None, alias="Submix")
    bleep: Optional[int] = Field(None, alias="Bleep")
    deess: Optional[int] = Field(None, alias="Deess")


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

    is_toggle: Optional[bool] = Field(None, alias="IsToggle")
    mute_type: Optional[str] = Field(None, alias="MuteType")
    state: Optional[str] = Field(None, alias="State")


class Colours(DefaultBaseModel):
    """Colours Model"""

    colour_one: Optional[str] = Field(None, alias="ColourOne")
    colour_two: Optional[str] = Field(None, alias="ColourTwo")


class Fader(DefaultBaseModel):
    """Fader Model"""

    style: Optional[str] = Field(None, alias="Style")
    colours: Optional[Colours] = Field(None, alias="Colours")


class Faders(DefaultBaseModel):
    """Faders Model"""

    a: Optional[Fader] = Field(None, alias="A")
    b: Optional[Fader] = Field(None, alias="B")
    c: Optional[Fader] = Field(None, alias="C")
    d: Optional[Fader] = Field(None, alias="D")


class Button(DefaultBaseModel):
    """Button Model"""

    off_style: Optional[str]
    colours: Optional[Colours]


class Buttons(DefaultBaseModel):
    """Buttons Model"""

    bleep: Optional[Button] = Field(None, alias="Bleep")
    fader1_mute: Optional[Button] = Field(None, alias="Fader1Mute")
    fader2_mute: Optional[Button] = Field(None, alias="Fader2Mute")
    fader3_mute: Optional[Button] = Field(None, alias="Fader3Mute")
    fader4_mute: Optional[Button] = Field(None, alias="Fader4Mute")
    cough: Optional[Button] = Field(None, alias="Cough")


class Global(DefaultBaseModel):
    """Global Model"""

    colour_one: Optional[str]


class Accent(DefaultBaseModel):
    """Accent Model"""

    colour_one: Optional[str]


class Simple(DefaultBaseModel):
    """Simple Model"""

    global_: Optional[Global] = Field(None, alias="Global")
    accent: Optional[Accent] = Field(None, alias="Accent")


class Lighting(DefaultBaseModel):
    """Lighting Model"""

    faders: Optional[Faders]
    buttons: Optional[Buttons]
    simple: Optional[Simple]
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

    fader1_mute: Optional[bool] = Field(None, alias="Fader1Mute")
    fader2_mute: Optional[bool] = Field(None, alias="Fader2Mute")
    fader3_mute: Optional[bool] = Field(None, alias="Fader3Mute")
    fader4_mute: Optional[bool] = Field(None, alias="Fader4Mute")
    bleep: Optional[bool] = Field(None, alias="Bleep")
    cough: Optional[bool] = Field(None, alias="Cough")
    effect_select1: Optional[bool] = Field(None, alias="EffectSelect1")
    effect_select2: Optional[bool] = Field(None, alias="EffectSelect2")
    effect_select3: Optional[bool] = Field(None, alias="EffectSelect3")
    effect_select4: Optional[bool] = Field(None, alias="EffectSelect4")
    effect_select5: Optional[bool] = Field(None, alias="EffectSelect5")
    effect_select6: Optional[bool] = Field(None, alias="EffectSelect6")
    effect_fx: Optional[bool] = Field(None, alias="EffectFx")
    effect_megaphone: Optional[bool] = Field(None, alias="EffectMegaphone")
    effect_robot: Optional[bool] = Field(None, alias="EffectRobot")
    effect_hard_tune: Optional[bool] = Field(None, alias="EffectHardTune")
    sampler_select_a: Optional[bool] = Field(None, alias="SamplerSelectA")
    sampler_select_b: Optional[bool] = Field(None, alias="SamplerSelectB")
    sampler_select_c: Optional[bool] = Field(None, alias="SamplerSelectC")
    sampler_top_left: Optional[bool] = Field(None, alias="SamplerTopLeft")
    sampler_top_right: Optional[bool] = Field(None, alias="SamplerTopRight")
    sampler_bottom_left: Optional[bool] = Field(None, alias="SamplerBottomLeft")
    sampler_bottom_right: Optional[bool] = Field(None, alias="SamplerBottomRight")
    sampler_clear: Optional[bool] = Field(None, alias="SamplerClear")


class Mixer(DefaultBaseModel):
    """Mixer Model"""

    hardware: Optional[Hardware]
    shutdown_commands: Optional[list]
    fader_status: Optional[FaderStatuses]
    mic_status: Optional[MicStatus]
    levels: Optional[Levels]
    router: Optional[Router]
    cough_button: Optional[CoughButton]
    lighting: Optional[Lighting]
    effects: Optional[Any]
    sampler: Optional[Any]
    settings: Optional[Settings]
    button_down: Optional[ButtonDown]
    profile_name: Optional[str]
    mic_profile_name: Optional[str]


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
