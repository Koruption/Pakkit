from simple_renderer import (
    Renderable,
    Question,
    Selection,
    TypedBlock,
    TypedText,
    Scene,
    Text,
    defer,
    Line,
    Point,
    Graphics,
    option,
    Group,
)
from pathlib import Path
from typing import List
from db import db
import utils


class LogoDisplay(TypedBlock):
    def __init__(self):
        super().__init__(
            db["scenes"]["bootup"]["logo"], hide_after_render=False, static=True
        )
        return

    def cached_render(self):
        return "\n".join(self.lines)


class BootupCreditsDisplay(TypedBlock):
    def __init__(self):
        super().__init__(
            db["scenes"]["bootup"]["credits"], hide_after_render=False, static=True
        )
        return

    def cached_render(self):
        return "\n".join(self.lines)


class BootupLogsDisplay(TypedBlock):
    def __init__(self):
        super().__init__(
            db["scenes"]["bootup"]["logs"], hide_after_render=False, static=True
        )
        return

    def cached_render(self):
        return "\n".join(self.lines)


class BarSpinnerDisplay(Renderable):
    def __init__(self):
        super().__init__(readable=False)
        return

    def render(self):
        self.disabled = True
        return utils.bar_spinner("$: ", 0.05)


class LineDisplay(Renderable):
    def __init__(self):
        self.gfx = Graphics()
        points = Line(Point.origin(), Point.rand_point(20)).points
        for p in points:
            self.gfx.move(p).draw("*")
        super().__init__(readable=False)
        return

    def render(self):
        return self.gfx.render()


class FileReaderDisplay(TypedBlock):
    def __init__(self, paths: List[str]):
        self.paths = paths
        self._engine._context.set(files=paths)
        super().__init__(paths, hide_after_render=True)
        return

    def render(self):
        return super().render()


class FileHandlerDisplay(Question):
    def __init__(self):
        super().__init__("Ready? 👋 Drop in a pak structured folder to begin...")
        return

    def on_response(self, path: str):
        # stub
        files = [path] * 12
        self.append_node(FileReaderDisplay(files))
        return


class HomeDisplay(Renderable):
    def __init__(self):
        super().__init__(readable=False)
        return

    @defer("files")
    def render(self):
        return utils.type_text(db["scenes"]["home"]["text"], 0.05)


home_scene: Scene = Scene(
    [
        Group(
            [
                LogoDisplay(),
                BootupCreditsDisplay(),
                BootupLogsDisplay(),
                BarSpinnerDisplay(),
            ],
            hide_after_render=True,
        ),
        FileHandlerDisplay(),
        HomeDisplay(),
    ]
)
