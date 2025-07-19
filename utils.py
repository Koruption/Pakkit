import time
import random
import os
import sys
import threading
from typing import Any, Callable, List
from enum import Enum
from alive_progress import alive_bar, styles
from alive_progress.styles import showtime
from audio import TrackInfo
from rich.console import Console
from rich.table import Table
from rich.align import Align

def test():
    return 

class ForegroundColor(Enum):
    Black = 30
    Red = 31
    Green = 32
    Yellow = 33
    Blue = 34
    Magenta = 35
    Cyan = 36
    White = 37


class BackgroundColor(Enum):
    Black = 40
    Red = 41
    Green = 42
    Yellow = 43
    Blue = 44
    Magenta = 45
    Cyan = 46
    White = 47


class ANSIStyle(Enum):
    Reset = 0
    Bold = 1
    Dim = 2
    Italic = 3
    Underline = 4
    Blink = 5
    Invert = 7
    Hidden = 8


class ANSIColor:

    def __init__(
        self,
        color: ForegroundColor,
        background: BackgroundColor = BackgroundColor.Black,
        style: ANSIStyle = ANSIStyle.Reset,
    ):
        self.color = color
        self.background = background
        self.style = style

    def colorize(self, text: str):
        return self.prefix() + text + self.suffix()

    def prefix(self):
        return f"\033[{self.style.value};{self.color.value};{self.background.value}m"

    def suffix(self):
        return f"\033[{self.style.value}m"


def colorize(char: str, level: int) -> str:
    # Map level 0-7 to color (lower = dim, higher = bright)
    colors = [
        "\033[38;5;240m",  # grey
        "\033[38;5;245m",  # lighter grey
        "\033[38;5;248m",
        "\033[38;5;250m",
        "\033[38;5;153m",  # soft blue
        "\033[38;5;75m",  # bright blue
        "\033[38;5;45m",  # cyan
        "\033[38;5;51m",  # aqua
    ]
    return f"{colors[level]}{char}\033[0m"


def type_line(text: str, delay: float = 0.5, new_line: bool = True):
    scaled = delay / 100
    for i in range(len(text)):
        print(f"\r{text[:i]}", end="", flush=True)
        time.sleep(scaled)
    if new_line:
        print("")


def type_text(lines: List[str], delay: float = 0.5, new_line: bool = True):
    for line in lines:
        type_line(line, delay, True)
    if new_line:
        print("")


def writ_to_line(text: str):
    clear_line()
    print(f"\r\033[K{text}", end="", flush=True)
    return


def clear_line():
    print("\r\033[K", end="")
    return


def clear_line_and_flush():
    sys.stdout.write("\r\033[K")
    sys.stdout.flush()
    return


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")
    return


class Bootup:

    logs = [
        "$ Initializing NERAVERSE kernel...",
        "$ Mounting /pak/core/",
        "$ Detecting audio nodes...",
        "$ Sourcing waveform matrix... OK",
        "$ Calibrating dynamic gain bus...",
        "$ Syncing vibrational lattice...",
        "$ Scanning for .pak structures... FOUND",
        "$ Verifying temporal harmonics... OK",
        "$ Bootstrapping Nera AudioPak Builder v1.0",
        "$ Allocating memory for transient audio fields...",
        "$ Checking integrity of spectral cache...",
        "$ Loading manifest.json... OK",
        "$ Connecting to NERAVERSE relay...",
        "$ Compiling acoustic geometry...",
        "$ Mapping signal path... OK",
        "$ Reconstructing waveform holograms...",
        "$ Initializing DSP tunnel...",
        "$ Activating meta-packet carrier...",
        "$ NeraPak interface online. Ready.",
    ]

    def __init__(self, delay: float = 0.08):
        self.delay = delay

    def print_logo(self):
        lines = [
            "-------------------------------------------------------------------------------------------",
            " ",
            "     .-') _   ('-.  _  .-')     ('-.             _ (`-.    ('-.    .-. .-')   .-')    ",
            "    ( OO ) )_(  OO)( \\( -O )   ( OO ).-.        ( (OO  )  ( OO ).-.\\  ( OO ) ( OO ).  ",
            ",--./ ,--,'(,------.,------.   / . --. /       _.`     \\  / . --. /,--. ,--.(_)---\\_) ",
            "|   \\ |  |\\ |  .---'|   /`. '  | \\-.  \\       (__...--''  | \\-.  \\ |  .'   //    _ |  ",
            "|    \\|  | )|  |    |  /  | |.-'-'  |  |       |  /  | |.-'-'  |  ||      /,\\  :` `.  ",
            "|  .     |/(|  '--. |  |_.' | \\| |_.'  |       |  |_.' | \\| |_.'  ||     ' _)'..`''.) ",
            "|  |\\    |  |  .--' |  .  '.'  |  .-.  |       |  .___.'  |  .-.  ||  .   \\ .-._)   \\ ",
            "|  | \\   |  |  `---.|  |\\  \\   |  | |  |       |  |       |  | |  ||  |\\   \\       / ",
            "`--'  `--'  `------'`--' '--'  `--' `--'       `--'       `--' `--'`--' '--' `-----'  ",
            " ",
            "                                         v1.0                                             ",
            "                               Corposoft© Software 2025                                    ",
            "                                  All rights reserved                                    ",
            " ",
            "-------------------------------------------------------------------------------------------",
        ]
        for line in lines:
            print(line)
            time.sleep(self.delay)
        return

    def print_bootup_logs(self):
        logs = [self.logs[random.randint(0, len(self.logs) - 1)] for _ in range(5)]

        bar_spinner("$", 0.02)
        for log in logs:
            type_line(log, 0.006)
            print("")
            time.sleep(0.05)
        return

    def clear(self):
        clear_terminal()
        return


def bar_spinner(label: str, delay: float = 0.4, amount: int = 15):
    char = ["\\", "|", "/", "-"]
    for i in range(amount):
        print(f"\r{label}{char[i % 4]}", end="", flush=True)
        time.sleep(random.random() * delay)
    print("\n")
    return

class BarSpinner:

    def __init__(self, label: str, delay: float = 0.4):
        self.label = label
        self.delay = delay
        self.play = False
        self._thread = None

    def _run(self):
        char = ["\\", "|", "/", "-"]
        for i in range(15):
            print(f"\r{self.label}{char[i % 4]}", end="", flush=True)
            time.sleep(random.random() * self.delay)
        print("\n")
        return

    def start(self, progressor: Callable[[None], Any]):
        if self.play:
            return
        self.play = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        result = progressor()
        self.__stop()
        return result

    def __stop(self):
        self.play = False
        if self._thread is not None:
            self._thread.join()
        writ_to_line("")

class AudioAnimation:

    def __init__(self, delay: float = 0.1):
        self.chars = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
        self.delay = delay
        self.play = False
        self._thread = None

    def _run(self):
        levels = [0, 0, 0]

        while self.play:
            # Randomly bump levels or decay
            for i in range(len(levels)):
                if random.random() < 0.3:
                    levels[i] = min(7, levels[i] + random.randint(1, 3))
                else:
                    levels[i] = max(0, levels[i] - 1)

            bars = "".join([colorize(self.chars[lv], lv) for lv in levels])
            writ_to_line(bars)
            time.sleep(self.delay)

    def start(self):
        if self.play:
            return
        self.play = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self.play = False
        if self._thread is not None:
            self._thread.join()
        writ_to_line("")

class AudioBar:
    def __init__(self, label="🎵 Playing track..."):
        self._stop = False
        self._thread = None
        self.label = label

    def _run(self):
        from alive_progress import styles
        with alive_bar(
            total=None,
            title=self.label,
            bar=styles.BARS['notes'],       # musical bouncing animation
            spinner=styles.SPINNERS['pulse'],    # smooth flowing spinner
        ) as bar:
            while not self._stop:
                bar()           # animate
                time.sleep(0.1)

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop = False
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop = True
        if self._thread:
            self._thread.join()

class Messenger:
    def type_lines(self, lines: List[str], delay=0.05, new_line=True):
        type_text(lines, delay, new_line)

    def type_text(self, text: str, delay=0.05, new_line=True):
        type_text(text, delay, new_line)

    def write_line(self, msg: str):
        writ_to_line(msg)

    def clear_line(self, flush: bool = False):
        if flush:
            clear_line_and_flush()
        else:
            clear_line()

    def new_line(self):
        print("\n")

    def clear(self):
        clear_terminal()


class NTable:

    def __init__(self, title: str, columns: List[str], rows: List[List[str]], highlight_row_no: int = None):
        self.columns = columns
        self.rows = rows
        self.console = Console()
        self.table = Table(title=title, expand=True)
        
        for col in self.columns:
            self.table.add_column(col, justify="right", style="cyan", no_wrap=True)
        for row in self.rows:
            if highlight_row_no is not None and row == self.rows[highlight_row_no]:
                self.table.add_row(*row, style="bold white on black")
            else:
                self.table.add_row(*row)

    def display(self):
        self.console.print(Align.center(self.table))


def debug_log(*args, fg: ForegroundColor=ForegroundColor.White, bg: BackgroundColor=BackgroundColor.Black):
    print(ANSIColor(fg, bg).colorize("[DEBUG] " + " ".join(map(str, args))))