from audio import AudioManager
from files import FileHandler, TempTree
from typing import Dict, List
from modes import ModeHandler, PlaybackMode, DefaultMode, PruningMode
from schemas import Mode, SessionEvents, SessionState
from graphics import Graphics
from events import Events
from stream import IoManager, IoStream
from utils import Messenger
import atexit

class ModeManager:
    def __init__(self, modes: Dict[Mode, ModeHandler]):
        self.modes = modes

        return

    def switch_mode(self, mode: Mode):
        for key, value in self.modes.items():
            if value.enabled:
                value.disable()
            if key == mode and not value.enabled:
                value.enable()

    def current(self):
        for key, value in self.modes.items():
            if value.enabled:
                return key
        return None

class Session:

    _instance: "Session" = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Session, cls).__new__(cls)
            cls.events: Events = Events()
            cls.io: IoManager = IoManager()
            cls.file_handler: FileHandler = FileHandler(cls)
            cls.temptree: TempTree = TempTree(cls)
            cls.audio_manager: AudioManager = AudioManager(cls)
            cls.sys_messenger: Messenger = Messenger()
            cls.graphics: Graphics = Graphics()
            cls.state: SessionState = SessionState()
            cls.mode_manager: ModeManager = ModeManager(
                {
                    Mode.PLAYBACK: PlaybackMode(cls),
                    Mode.DEFAULT: DefaultMode(cls),
                    Mode.PRUNING: PruningMode(cls),
                }
            )
            cls.events.on(SessionEvents.tree_loaded, lambda tree: cls.mode_manager.switch_mode(Mode.DEFAULT))
            cls.events.on(SessionEvents.default_mode_ended, lambda: cls.mode_manager.switch_mode(Mode.PLAYBACK))
            cls.events.on(SessionEvents.playback_mode_ended, lambda: cls.mode_manager.switch_mode(Mode.DEFAULT))
            cls.events.on(SessionEvents.pruning_mode_ended, lambda: cls.mode_manager.switch_mode(Mode.DEFAULT))

        return cls._instance

    def start(self):
        self.io.start()
        IoStream.start()
        self.events.emit(SessionEvents.session_started)
        atexit.register(Session.sigint_exit)
        return

    def sigint_exit():
        try:
            FileHandler.clear_temp()
        except KeyboardInterrupt:
            pass

    def stop(self):
        IoStream.stop()
        self.io.stop()
        self.events.emit(SessionEvents.session_ended)
        return
