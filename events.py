import uuid
from typing import Any, Callable, Dict, List
from schemas import SessionEvents

class EventResponder:
    def __init__(self, callback: Callable[[Any], None], once: bool = False):
        self.callback: Callable = callback
        self.once: bool = once
        self._id: uuid.UUID = uuid.uuid4()

    def id(self):
        return self._id

class Events:

    def __init__(self):
        self._registry: Dict[SessionEvents, List[EventResponder]] = {}

    def on(self, event: SessionEvents, callback: Callable[[Any], None], once: bool = False):
        if event not in self._registry:
            self._registry[event] = []
        self._registry[event].append(EventResponder(callback, once))

    def emit(self, event: SessionEvents, *args, **kwargs):
        if event in self._registry:
            for responder in self._registry[event]:
                # print(f"Emitting {event} to {responder.callback}")
                if (responder.callback is None):
                    continue
                responder.callback(*args, **kwargs)
                if responder.once:
                    self._registry[event].remove(responder)

