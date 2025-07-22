from lib.primitives import Readable, Renderable
from typing import (
    List,
    TypeVar,
)
from lib.events import EngineEvents
from lib.diffing import DiffEngine
from threading import Thread
import utils
import time

T = TypeVar("T")


class Renderer:

    def __init__(self, events: EngineEvents, diffing: DiffEngine):
        self.events = events
        self.diffing = diffing
        self._last_time = 0
        self.buffer: List[Renderable] = []
        self.exit_flag = False
        self.first_pass = False

    def set_buffer(self, buffer: List[Renderable]):
        self.buffer = buffer
        self.events.emit("buffer-set", self.buffer)
        return

    def clear_screen(self):
        utils.clear_terminal()

    def should_remove(self, renderable: Renderable):
        return renderable.should_remove or renderable.render_once

    def should_diff(self, renderable: Renderable):
        # print({
        #     "first_pass": self.first_pass,
        #     "renderable": renderable.render_once,
        #     "cacheable": renderable.cacheable
        # })
        return not self.first_pass and not renderable.render_once

    def _call_ticks(self, delta_time):
        for r in self.buffer:
            r.on_tick(delta_time)

    def _call_starts(self):
        for r in self.buffer:
            r.did_start = True
            r.on_start()

    def is_scene_dirty(self):
        for renderable in self.buffer:
            if self.should_diff(renderable) and self.diffing.diff(renderable):
                print(f"Diff found on: {renderable.__class__.__name__}")
                return True

    def loop(self):
        while not self.exit_flag:
            now = time.time()
            delta_time = now - self._last_time
            self._last_time = now

            if self.first_pass:
                self._call_starts()

            if self.is_scene_dirty():
                self.clear_screen()
            for i, renderable in enumerate(self.buffer):
                if renderable.defer_render:
                    continue

                if renderable.should_use_cache():
                    print(renderable.render_cached())
                    continue

                if not isinstance(renderable, Readable):
                    renderable.render()
                    if self.should_remove(renderable):
                        self.buffer[i] = None
                    renderable.post_render()

                else:
                    response = renderable.render()
                    _renderables = renderable.on_response(response)
                    renderable.post_render()
                    if self.should_remove(renderable):
                        self.buffer[i] = None
                    if _renderables is not None and isinstance(_renderables, list):
                        self.buffer[i + 1 : i + 1] = _renderables
                        # re-render top-down if new nodes are inserted
                        break
                    elif _renderables is not None:
                        self.buffer.insert(i + 1, _renderables)
                        # re-render top-down if new nodes are inserted
                        break

            self.first_pass = False
            self.buffer = [r for r in self.buffer if r is not None]
            self._call_ticks(delta_time)

    def get_thread(self):
        return Thread(target=self.loop)
