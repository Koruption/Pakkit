from typing import Callable, Any
from threading import Thread
from dataclasses import dataclass

@dataclass
class ProcessHandle:
    cb: Callable
    done: bool
    

class Process:

    def __init__(self, cb: Callable[[Any], None]):
        self.cb = cb



Process(run_animation)