import sys
import os
import tty
import termios
from typing import List, Any, Callable
from dataclasses import dataclass
from schemas import OutputType, Output
from enum import Enum

def init_terminal():
    """Initialize terminal for raw input"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    new_settings = termios.tcgetattr(fd)
    new_settings[3] = new_settings[3] & ~(termios.ECHO | termios.ICANON)  # lflags
    termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)
    return old_settings

def restore_terminal(old_settings):
    """Restore terminal to normal state"""
    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
from threading import Thread
import time
import utils
import questionary
from pynput import keyboard

class InputType(Enum):
    KEY = 1
    RESPONSE = 2

@dataclass
class InputData:
    type: InputType
    data: Any

    def is_key(self):
        return self.type == InputType.KEY

    def is_response(self):
        return self.type == InputType.RESPONSE

class IoStream:
    _stream: List[InputData] = []
    callbacks: List[Callable[[InputData], None]] = []
    _tick: bool = False
    _listener: keyboard.Listener = None
    _tracking_keyboard_events: bool = False

    def _write(data: InputData):
        IoStream._stream.append(data)
        for callback in IoStream.callbacks:
            callback(data)

    def listen(callback: Callable[[InputData], None]):
        IoStream.callbacks.append(callback)

    def read():
        if len(IoStream._stream) == 0:
            return None
        return IoStream._stream.pop(0)

    def track_keyboard_events():
        IoStream._tracking_keyboard_events = True
        IoStream._listener = keyboard.Listener(on_press=IoStream._handle_key)
        IoStream._listener.start()

    def stop_tracking_keyboard_events():
        IoStream._tracking_keyboard_events = False
        IoStream._listener.stop()

    def start():
        IoStream._tick = True
        return IoStream._listener

    def stop():
        IoStream._tick = False
        IoStream.stop_tracking_keyboard_events()
        return

    def _handle_key(key: keyboard.Key):
        if not IoStream._tracking_keyboard_events:
            return
        IoStream._write(InputData(InputType.KEY, key))

class IoManager:
    _instance: "IoManager" = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(IoManager, cls).__new__(cls)
            cls._instance.queue: List[Output] = []
            cls._instance._tick = False
        return cls._instance

    def write(
        self,
        message: str,
        output_type: OutputType,
        onResponse: Callable[[str], None] = None,
        data: Any = None,
    ):
        if output_type == OutputType.error:
            self.queue = [Output(message, output_type, onResponse, data)] + self.queue
            return
        if output_type == OutputType.sigint:
            sys.exit(0)

        self.queue.append(Output(message, output_type, onResponse, data))

    def pop_queue_head(self):
        if len(self.queue) > 0:
            return self.queue.pop(0)
        return None

    def tick():
        while IoStream._tick:
            output = IoStream.read()
            if output:
                if output.is_key():
                    IoStream._write(InputData(InputType.KEY, output.data))
                elif output.is_response():
                    IoStream._write(InputData(InputType.RESPONSE, output.data))
            time.sleep(0.3)
        return

    def tick(self):
        while self._tick:
            output = self.pop_queue_head()
            if output:
                if output.type == OutputType.question:
                    response = questionary.text(output.message).ask()
                    IoStream._write(InputData(InputType.RESPONSE, response))
                    if output.onResponse:
                        output.onResponse(response)
                elif output.type == OutputType.error:
                    print(f"Error: {output.message}")
                elif output.type == OutputType.text:
                    print(output.message)
                elif output.type == OutputType.selection:
                    response = questionary.select(
                        output.message, choices=output.data
                    ).ask()
                    IoStream._write(InputData(InputType.RESPONSE, response))
                    if output.onResponse:
                        output.onResponse(response)
            time.sleep(0.3)  # sleep for 300ms
        return

    def start(self):
        self._old_term_settings = init_terminal()
        self._tick = True
        thread = Thread(target=self.tick) # adding daemon=True breaks sigint handling
        thread.start()
        return thread

    def stop(self):
        self._tick = False
        restore_terminal(self._old_term_settings)
        return

    def stop(self):
        self._tick = False
        return

    def clear(self):
        utils.clear_terminal()
        return
