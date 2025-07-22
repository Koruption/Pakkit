from typing import List, Callable, Any
from threading import Thread
import termios
import time
import sys
import tty

class InputStream:

    instance: "InputStream"

    def __init__(self, poll_frq=0.1):
        self._stop_flag = False
        self._poll_frq = poll_frq
        self._fd = sys.stdin.fileno()
        self._old_settings = termios.tcgetattr(self._fd)
        self._listeners: List[Callable[[str], Any]] = []
        self._io_thread:Thread = None

        InputStream.instance = self

    def on(self, cb: Callable[[str], Any]):
        self._listeners.append(cb)


    def get_instance():
        return InputStream.instance

    def _dispatch_to_listeners(self, ch: str):
        for cb in self._listeners:
            cb(ch)
        return 
    
    def poll(self):
        tty.setraw(self._fd)
        try:
            while not self._stop_flag:
                ch = sys.stdin.read(1)
                self._dispatch_to_listeners(ch)
                time.sleep(self._poll_frq)
        finally:
            termios.tcsetattr(self._fd, termios.TCSADRAIN, self._old_settings)

    def start(self):
        self._io_thread = Thread(target=self.poll)
        self._io_thread.start()

    def stop(self):
        self._stop_flag = True
        self._io_thread.join()

class Stream:
    def __init__(self, buffer_size=1000):
        self._buffer: List[str] = []
        self._buffer_size = buffer_size
        InputStream.instance.on(self._on_input)

    def _on_input(self, char: str):
        if len(self._buffer) > self._buffer_size: self._buffer.pop(0)
        self._buffer.append(char)

    def read(self):
        self._buffer.pop()
        return 

class InputHandler:

    def __init__(self, stream: Stream):
        self.stream = stream
        return 