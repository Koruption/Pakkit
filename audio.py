# from session import Session # keep commented out for circular dependency
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from files import TempTree
from schemas import SessionEvents
from schemas import OutputType
from pathlib import Path
from mutagen.mp3 import MP3
from typing import TYPE_CHECKING, List, Callable
import threading
import time

if TYPE_CHECKING:
    from session import Session  # for static checking only

class TrackInfo:

    def __init__(self, path: Path):
        self.name = path.name
        self.path = path

    def get_duration(self):
        try:
            return MP3(self.path).info.length
        except Exception as e:
            return 0

    def get_duration_str(self):
        secs = int(self.get_duration())
        mins = secs // 60
        secs = secs % 60
        return f"{mins}:{secs:02d}"


class AudioManager:

    def __init__(self, session: "Session"):
        self.assets = []
        self.playing = False
        self.track_index = 0
        self.session: Session = session
        self._progress = 0
        self._progess_callbacks: List[Callable[[float], None]] = []
        self.on_track_changed_callbacks: List[Callable[[TrackInfo], None]] = []

        self.session.events.on(SessionEvents.tree_loaded, self._on_tree_loaded)
        

    def _on_tree_loaded(self, tree: TempTree):
        self.assets = (
            [TrackInfo(track) for track in TempTree.tracks()]
            + [TrackInfo(TempTree.intro())]
            + [TrackInfo(interrupt) for interrupt in TempTree.interrupts()]
            + [TrackInfo(sfx) for sfx in TempTree.sfx()]
        )
        self.load()

    def on_progress(self, callback: Callable[[float], None]):
        self._progess_callbacks.append(callback)

    def on_track_changed(self, callback: Callable[[TrackInfo], None]):
        self.on_track_changed_callbacks.append(callback)

    def call_on_track_changed(self, track: TrackInfo):
        for callback in self.on_track_changed_callbacks:
            callback(track)

    def call_on_progress(self, progress: float):
        for callback in self._progess_callbacks:
            callback(progress)

    def load(self):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.3)
        for asset in self.assets:
            try:
                pygame.mixer.music.load(asset.path)
            except Exception as e:
                print("")
                self.session.io.write(
                    f"Failed to load asset: {asset.path} /", OutputType.error
                )
                self.session.io.write(f"├─ Error: {e}", OutputType.error)
        self.call_on_track_changed(self.assets[self.track_index])

    def volume_up(self):
        pygame.mixer.music.set_volume(min(1.0, pygame.mixer.music.get_volume() + 0.1))

    def volume_down(self):
        pygame.mixer.music.set_volume(max(0.0, pygame.mixer.music.get_volume() - 0.1))

    def _play(self):
        if not self.assets:
            return
        if not self.playing:
            self._resume()
        else:
            self.playing = True
            self._play_current_track()

        # Start background watcher thread
        threading.Thread(target=self._watch_playback, daemon=True).start()

    def toggle_play(self):
        if self.playing:
            self._pause()
        else:
            self._play()

    def _resume(self):
        if not self.playing:
            self.playing = True
            pygame.mixer.music.unpause()

    def _pause(self):
        if not self.playing:
            return
        self.playing = False
        pygame.mixer.music.pause()

    def get_progress(self):
        if duration == 0:
            return 0.0
        return self._progress / self.assets[self.track_index].get_duration()

    def _play_current_track(self):
        try:
            pygame.mixer.music.load(self.assets[self.track_index].path)
            pygame.mixer.music.play( fade_ms=5000 )
        except Exception as e:
            self.session.io.write(
                f"Failed to play asset: {self.assets[self.track_index].path}", OutputType.error
            )
            self.session.io.write(f"├─ Error: {e}", OutputType.error)
            self.next_track()

    def _watch_playback(self):
        while self.playing:
            if not pygame.mixer.music.get_busy():
                time.sleep(0.5)  
                self.next_track()
                self._play_current_track()
                self._progress = 0
            time.sleep(0.1)
            self._progress += 0.1
            self.call_on_progress(self._progress)

    def set_track(self, index: int):
        if index < 0 or index >= len(self.assets):
            return
        self.track_index = index

    def next_track(self):
        # self.session.sys_messenger.clear()
        # self.session.sys_messenger.write_line("\nPlaying next track...")
        if (self.track_index + 1) >= len(self.assets):
            self.set_track(0)
            self._play_current_track()
            self.call_on_track_changed(self.assets[self.track_index])
            return
        self.set_track((self.track_index + 1) % len(self.assets))
        self._play_current_track()
        self.call_on_track_changed(self.assets[self.track_index])

    def previous_track(self):
        # self.session.sys_messenger.clear()
        # self.session.sys_messenger.write_line("\nPlaying previous track...")
        if (self.track_index - 1) < 0:
            self.set_track(len(self.assets) - 1)
            self._play_current_track()
            self.call_on_track_changed(self.assets[self.track_index])
            return
        self.set_track((self.track_index - 1) % len(self.assets))
        self._play_current_track()
        self.call_on_track_changed(self.assets[self.track_index])

    def get_current_track(self):
        return self.assets[self.track_index]

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False
