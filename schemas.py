from dataclasses import dataclass
from typing import List, Callable, Any
from enum import Enum

"""
MyCoolPak/
├── metadata.json         ← required: title, author, bpm, etc.
├── cover.png             ← optional: cover art or gif
├── intro.mp3             ← optional: intro clip
├── tracks/
│   ├── track1.mp3
│   ├── track2.mp3
│   └── ...
├── sfx/
│   ├── sfx1.wav         ← optional: sound effects
│   └── ...
├── interrupts/
│   ├── interrupt1.wav        ← optional: SFX / vocals
│   └── ...
└── README.md             ← optional: artist notes, license, etc.
"""


class Rarity(Enum):
    common = "common"
    rare = "rare"
    epic = "epic"


class SegmentType(Enum):
    interrupt = "interrupt"
    music = "music"


@dataclass
class Paket:
    name: str
    segmentType: SegmentType
    rarity: Rarity
    duration: int
    localUrl: str


@dataclass
class AudioPak:
    name: str
    description: str
    author: str
    version: str
    date: str
    pakets: List[Paket]

class OutputType(Enum):
    question = "question"
    error = "error"
    text = "text"
    selection = "selection"
    sigint = "sigint"

@dataclass
class Output:
    message: str
    type: OutputType
    onResponse: Callable[[str], None] = None
    data: Any = None

class SessionEvents(Enum):
    file_dropped = "file_dropped"
    tree_loaded = "tree_loaded"
    pak_validated = "pak_validated"
    session_started = "session_started"
    session_ended = "session_ended"
    playback_mode_started = "playback_mode_started"
    playback_mode_ended = "playback_mode_ended"
    default_mode_started = "default_mode_started"
    default_mode_ended = "default_mode_ended"
    pruning_mode_started = "pruning_mode_started"
    pruning_mode_ended = "pruning_mode_ended"

class Mode(Enum):
    DEFAULT = "default"
    PLAYBACK = "playback"
    PRUNING = "pruning"

class SessionState:
    def __init__(self):
        self.pak_name: str = ""
        self.pak_description: str = ""
        self.pak_author: str = ""
        self.pak_version: str = ""
        return
    