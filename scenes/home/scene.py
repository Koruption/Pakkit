from simple_renderer import (
    Readable,
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
    Engine,
)
from pathlib import Path
from files import FileHandler, TempTree
from typing import List
from db import db
import utils
import random
import time


class LogoDisplay(TypedBlock):
    def __init__(self, speed: float = 0.2):
        super().__init__(
            db["scenes"]["bootup"]["logo"],
            hide_after_render=False,
            static=True,
            speed=speed,
        )
        return

    def cached_render(self):
        return "\n".join(self.lines)


class BootupCreditsDisplay(TypedBlock):
    def __init__(self, speed: float = 0.1):
        super().__init__(
            (db["scenes"]["bootup"]["credits"]),
            hide_after_render=False,
            static=True,
            speed=speed,
        )
        return

    def cached_render(self):
        return "\n".join(self.lines)


class BootupLogsDisplay(TypedBlock):
    def __init__(self, speed: float = 0.1, log_size: int = 5):
        super().__init__(
            random.sample(
                db["scenes"]["bootup"]["logs"],
                log_size,
            ),
            hide_after_render=False,
            static=True,
            speed=speed,
        )
        return

    def cached_render(self):
        return "\n".join(self.lines)


class BarSpinnerDisplay(Renderable):

    def render(self):
        self.disabled = True
        return utils.bar_spinner("$: ", 0.2)


class LineDisplay(Renderable):
    def __init__(self):
        self.gfx = Graphics()
        points = Line(Point.origin(), Point.rand_point(20)).points
        for p in points:
            self.gfx.move(p).draw("*")
        super().__init__()
        return

    def render(self):
        return self.gfx.render()


class FileReaderDisplay(TypedBlock):
    def __init__(self, paths: List[Path]):
        self.paths: List[Path] = paths
        super().__init__(
            [],
            hide_after_render=False,
        )
        self.speed = 0.1
        return

    def on_start(self):
        self.ctx().set(files=self.paths)
        self.lines = [f" > Reading file: {path}" for path in TempTree.list_files()]
        return

    def render(self):
        if len(self.lines) == 0:
            return "[whoops] No files found in directory"
        return super().render()


class FileHandlerDisplay(Question):
    def __init__(self):
        super().__init__("Ready? 👋 Drop in a pak structured folder to begin...")
        return

    def on_start(self):
        self._engine._dependency_graph.add_edge(self, "file_size")
        return

    def after_render(self, ctx: "Context"):
        Engine.debug(
            "[file handler info] After render",
            fg=utils.ForegroundColor.Green,
            bg=utils.BackgroundColor.Black,
        )
        size = self.ctx().get("file_size")
        Engine.debug("[file handler info] File size from ctx.get('file_size')", size, trace=True)
        if size > 10:
            Engine.debug("[file handler info] File size exceeded 10MB", trace=True)
            self.append_node(
                Group(
                    [
                        FileReaderDisplay(TempTree.list_files()),
                        TypedBlock(
                            [
                                db["scenes"]["home"]["file_size_exceeded"],
                                f"Actual size: {size}MB",
                                "Drop in a smaller pak by typing 'new' or select prune to drop selected files",
                            ],
                            static=True,
                        ),
                    ],
                    hide_after_render=True,
                )
            )
        return

    def on_response(self, path: str):
        resp = FileHandler.process_file(path)
        if resp.valid:
            files = FileHandler.list_files(resp.path)
            FileHandler.copy_to_temp(resp.path)
            # self.ctx().set(files=files)
            size = FileHandler.calc_total_pak_size(resp.path)
            self.ctx().set(file_size=size)
            Engine.debug(f"Reachted this point ")
            Engine.debug()
            Engine.debug((f"[on_response] self id: {id(self)}"))
            Engine.debug((f"[on_response] self ctx id: {id(self.ctx())}"))
            Engine.debug((f"[on_response] engine ctx id: {id(Engine._context)}"))
            Engine.debug(f"[file handler info] File size: {size}")
            Engine.debug(
                "----------------------------------- Rednering FileHandlerDisplay -----------------------------------"
            )

        #     self.append_node(
        #         Group(
        #             [
        #                 TypedText("Directory integrity check passed... OK"),
        #                 TypedBlock(["..." for _ in range(5)], static=True),
        #                 FileReaderDisplay(files)
        #             ],
        #             hide_after_render=True,
        #         )
        #     ).append_node(FileReaderDisplay(files))
        # else:
        #     self.append_node(TypedText(self.ctx().get("file_handler_display"), static=True))
        return

    def render(self):
        return super().render()


class HomeDisplay(Readable):
    def __init__(self):
        super().__init__()
        return

    @defer("files")
    def render(self):
        time.sleep(0.2)
        return utils.type_text(db["scenes"]["home"]["overview"], 0.05)

    def cached_render(self):
        return "\n".join(db["scenes"]["home"]["overview"])


class HomeInputHandler(Question):
    def __init__(self):
        super().__init__(question=db["scenes"]["home"]["default_prompt"])
        return

    def on_response(self, response: str):
        print(response)
        return

    @defer("files")
    def render(self):
        return super().render()

    def cached_render(self):
        return db["scenes"]["home"]["default_prompt"]


Home: Scene = Scene(
    [
        Group(
            [
                LogoDisplay(speed=0.01),
                BootupCreditsDisplay(speed=0.01),
                BootupLogsDisplay(log_size=6, speed=0.01),
                BarSpinnerDisplay(),
                BootupLogsDisplay(log_size=3, speed=0.01),
                BarSpinnerDisplay(),
            ],
            hide_after_render=True,
        ),
        HomeDisplay(),
        FileHandlerDisplay(),
        # HomeInputHandler(),
    ]
)
