from typing import List
import utils
from message import messages
import time

class Graphics:
    def __init__(self):
        self._instance = None

    def display_boot(self):
        self.display_logo()
        self.display_bootup_logs()
        self.display_bar_spinner("", 0.1)
        self.clear()
        self.display_welcome()

    def display_colored_text(self, text: str, foreground: utils.ForegroundColor, background: utils.BackgroundColor):
        color = utils.ANSIColor(foreground, background)
        print(color.colorize(text))
    
    def display_logo(self):
        utils.Bootup().print_logo()

    def display_welcome(self):
        self.display_typed_lines(messages["welcome"], 0.07)

    def display_bootup_logs(self):
        utils.Bootup().print_bootup_logs()

    def display_typed_lines(self, lines: List[str], delay: float = 0.05, new_line: bool = True):
        utils.type_text(lines, delay, new_line)

    def display_typed_line(self, text: str, delay: float = 0.05, new_line: bool = True):
        utils.type_line(text, delay, new_line)

    def display_bar_spinner(self, label: str, delay: float = 0.4, amount: int = 15):
        utils.bar_spinner(label, delay, amount)

    def display_audio_animation(self, delay: float = 0.1):
        utils.AudioAnimation(delay).start()
        
    def clear_line(self):
        utils.clear_line()

    def clear(self):    
        utils.clear_terminal()