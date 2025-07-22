from enum import Enum
from typing import List, Callable, Dict, Any

class EventNames(Enum):
    BUFFER_SET = "buffer_set"
    ENGINE_START = "engine_start"
    ENGINE_STOPPED = "engine_stopped"
    SCENE_TRANSITION = "scene_transitioned"

class EngineEvents:

    def __init__(self):
        self._registry: Dict[EventNames, List[Callable[[Any], None]]] = {}
        return

    def on(self, event: str, cb: Callable[[Any], None]):
        if event not in self._registry:
            self._registry[event] = []
        self._registry[event].append(cb)

    def emit(self, event: EventNames, data=None):
        if event not in self._registry:
            return
        for cb in self._registry[event]:
            if data:
                cb(data)
            else:
                cb()

