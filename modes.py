from audio import AudioManager, TrackInfo
from schemas import OutputType, SessionEvents
from message import messages
from stream import IoStream, InputData
from typing import TYPE_CHECKING, List
from schemas import Mode
from pynput import keyboard
from datetime import datetime
import utils
from files import FileHandler, TempTree
from pathlib import Path

if TYPE_CHECKING:
    from session import Session  # for static checking only

class ModeHandler:
    enabled: bool = False

    def __init__(self, session: "Session"):
        self.session = session
        IoStream.listen(self._key_listener)
        return

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_key(self, key: keyboard.Key):
        pass

    def on_response(self, data: str):
        pass

    def enable(self):
        pass

    def disable(self):
        pass

    def _key_listener(self, input_data: InputData):
        if not self.enabled:
            return
        if input_data.is_key():
            self.on_key(input_data.data)
        if input_data.is_response():
            self.on_response(input_data.data)


class DefaultMode(ModeHandler):
    def __init__(self, session: "Session"):
        super().__init__(session)
        self.enabled = False
        return

    def handle_pak_selected(self, response: str):
        self.session.state.pak_name = response
        self.session.io.write("What is the description of your pak?", OutputType.question, self.handle_pak_description_selected)

    def handle_pak_description_selected(self, response: str):
        self.session.state.pak_description = response
        self.session.io.write("What is the author of your pak?", OutputType.question, self.handle_pak_author_selected)

    def handle_pak_author_selected(self, response: str):
        self.session.state.pak_author = response
        TempTree.write_metadata({
            "title": self.session.state.pak_name,
            "description": self.session.state.pak_description,
            "author": self.session.state.pak_author,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        self.session.io.write("Packing...", OutputType.text)
        spinner = utils.BarSpinner("")
        spinner.start(self.session.file_handler.pak_temp)
        self.session.io.clear()
        self.session.io.write("Done!", OutputType.text)
        self.session.io.write("Pak saved to: " + self.session.state.pak_name + ".pak", OutputType.text)
        self.session.io.clear()
        self.session.io.write(messages["default_mode_prompt"], OutputType.question)

    def on_response(self, data: str):
        if not self.enabled:
            return
        if data == "play":
            # self.session.mode_manager.switch_mode(Mode.PLAYBACK)
            self.session.io.write("\tᕕ(⌐■_■)ᕗ ♪♬", OutputType.text)
            self.disable()
            return
        if data == "upload":
            # do uploading
            pass
        elif data == "pack":
            self.session.io.clear()
            self.session.io.write("What is the name of your pak?", OutputType.question, self.handle_pak_selected)
            # do packing
            pass
        elif data == "new":
            # do new drag and drop
            pass
        elif data == "prune":
            self.session.mode_manager.switch_mode(Mode.PRUNING)
        elif data == "menu":
            # TODO: !!! implement menu !!!
            self.session.io.write(messages["default_mode_prompt"], OutputType.selection)
        else:
            self.session.sys_messenger.clear_line(flush=True)

    def enable(self):
        self.enabled = True
        self.session.io.clear()
        self.session.io.write(messages["default_mode_prompt"], OutputType.question)
        self.session.events.emit(SessionEvents.default_mode_started)

    def disable(self):
        self.enabled = False
        self.session.io.clear()
        self.session.events.emit(SessionEvents.default_mode_ended)


class PlaybackMode(ModeHandler):
    def __init__(self, session: "Session"):
        super().__init__(session)
        self.audio_manager: AudioManager = session.audio_manager
        self.enabled = False
        self._audio_bar: utils.AudioBar = utils.AudioBar()
        return

    def on_exit(self):
        self.audio_manager.stop()

    def handle_on_track_changed(self, track: TrackInfo):
        self._audio_bar.stop()
        self._audio_bar.start()
        self.draw_table()

    def enable(self):
        self.enabled = True
        self.session.io.clear()
        self.session.io.write(messages["playback_mode_prompt"], OutputType.selection, data=["Play/Pause", "Next", "Previous", "Exit", "Volume Up", "Volume Down"])
        self.audio_manager.load()
        self.audio_manager.on_track_changed(self.handle_on_track_changed)

    def draw_table(self):
        table = utils.NTable(
            "Audio Bar",
            ["Track", "Duration"],
            [
                [track.name, track.get_duration_str()]
                for track in self.audio_manager.assets
            ],
            self.audio_manager.track_index,
        )
        self.session.sys_messenger.clear()
        table.display()
        print("\n")
        self.session.io.write(messages["playback_mode_prompt"], OutputType.text)

        self.session.sys_messenger.write_line(
            f" > Playing {self.audio_manager.assets[self.audio_manager.track_index].name} | Duration: {self.audio_manager.assets[self.audio_manager.track_index].get_duration_str()} "
        )
        return

    def draw_controls(self):
        self.session.io.write(messages["playback_mode_prompt"], OutputType.selection, data=["Play/Pause", "Next", "Previous", "Exit", "Volume Up", "Volume Down"])

    def disable(self):
        IoStream.stop_tracking_keyboard_events()
        self.enabled = False
        if self.audio_manager.playing:
            self.audio_manager.stop()
        self._audio_bar.stop()
        self.session.io.clear()
        self.session.events.emit(SessionEvents.playback_mode_ended)

    def on_response(self, response: str):
        self.session.sys_messenger.clear_line(flush=True)
        if not self.enabled:
            return
        if response == "Exit":
            self.disable()
            return
        if response == "Volume Up":
            self.audio_manager.volume_up()
            self.draw_controls()
            return
        if response == "Volume Down":
            self.audio_manager.volume_down()
            self.draw_controls()
            return
        if response == "Play/Pause":
            self.audio_manager.toggle_play()
            if self.audio_manager.playing:
                self._audio_bar.start()
                self.session.sys_messenger.clear()
                self.draw_table()
            else:
                self._audio_bar.stop()
                self.session.sys_messenger.clear()
                self.draw_table()
            self.draw_controls()
            return
        if response == "Next":
            self.audio_manager.next_track()
            self.draw_controls()
            return
        if response == "Previous":
            self.audio_manager.previous_track()
            self.draw_controls()
            return
        else:
            self.session.sys_messenger.clear_line(flush=True)
            self.draw_controls()
            pass


class PruningMode(ModeHandler):
    def __init__(self, session: "Session"):
        super().__init__(session)
        self.enabled = False
        self.files: List[Path] = TempTree.list_files()
        self.selection_index: int = 0
        return

    def draw_table(self):
        table = utils.NTable(
            "Pruning Mode",
            ["File", "Size"],
            [
                [file.name, FileHandler.file_size_mb(file)]
                for file in self.files
            ],
            self.selection_index,
        )
        self.session.sys_messenger.clear()
        table.display()
        print("\n")
        self.write_prompt()

        self.session.sys_messenger.write_line(
            f" > Current selection: {self.files[self.selection_index].name} | File size: {FileHandler.file_size_mb(self.files[self.selection_index])} MB "
        )
        return

    def write_prompt(self):
        self.session.io.write(messages["pruning_mode_prompt"], OutputType.selection, data=["up", "down", "delete", "q"])

    def enable(self):
        print("=================================== PRUNING MODE ===================================")
        self.enabled = True
        self.session.io.clear()
        self.write_prompt()
        self.session.events.emit(SessionEvents.default_mode_started)
        return

    def disable(self):
        self.enabled = False
        self.session.io.clear()
        self.session.events.emit(SessionEvents.pruning_mode_ended)
        return

    def on_response(self, response: str):
        self.session.sys_messenger.clear_line(flush=True)
        if not self.enabled:
            return
        if response == "q":
            self.disable()
            return
        if response == "up":
            self.selection_index = max(0, self.selection_index - 1)
            self.draw_table()
            return
        if response == "down":
            self.selection_index = min(len(self.files) - 1, self.selection_index + 1)
            self.draw_table()
            return
        if response == "delete":
            self.files[self.selection_index].unlink()
            self.draw_table()
            return
        else:
            self.session.sys_messenger.clear_line(flush=True)
            self.write_prompt()
            pass
