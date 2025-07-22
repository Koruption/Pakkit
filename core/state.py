from typing import Dict, Generic, TypeVar, List, Callable, Any

T = TypeVar("T")

class EngineState:

    ctx: "EngineState"

    def __init__(self):
        self._store: Dict[str, "State"] = {}
        EngineState.ctx = self
        return

    def subscribe(self, key: str):
        import inspect

        frame = inspect.currentframe().f_back
        instance = frame.f_locals["self"]  # Get the instance from the local variables
        if key in self._store:
            self._store[key].watchers.append(instance)

    def _notify_watchers(self, state: "State"):
        for sub in state.watchers:
            sub(state.val)

    def set(self, state: "State"):
        if state.key in EngineState.ctx._store:
            if state.val == EngineState.ctx._store[state.key].val:
                return
            EngineState.ctx._store[state.key] = state
            return 
        EngineState.ctx._store[state.key]=state

    def get(self, key: str):
        if key in EngineState.ctx._store:
            return EngineState.ctx._store[key]
        return None


class State(Generic[T]):

    def __init__(self, key: str, val: T):
        self.key = key
        self.val: T = val
        self.watchers: List[Callable[[T], Any]] = []
        EngineState.ctx.set(self)

    def set(self, val: T):
        self.val = val
        EngineState.ctx.set(self)

    def get(self) -> T:
        EngineState.ctx.subscribe(self.key)
        return EngineState.ctx.get(self.key).val
