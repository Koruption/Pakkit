from typing import List, Dict, Any, TYPE_CHECKING, Callable, Union
from time import sleep
from threading import Thread
from functools import wraps
import os
import inspect
from rich.table import Table as RichTable
from rich.console import Console
from rich.align import Align
import questionary
import math
import random
import time

import utils
from dataclasses import dataclass
from typing import Tuple
import sys
import uuid
import atexit
import traceback

class Point:

    @staticmethod
    def origin() -> "Point":
        return Point(1, 1)

    @staticmethod
    def rand_point(range: int) -> "Point":
        return Point(random.randint(0, range), random.randint(0, range))

    def __init__(self, x: int, y: int):
        self.x: int = max(1, int(x + 1))
        self.y: int = max(1, int(y + 1))
        return

    def swap(self):
        self.x, self.y = self.y, self.x
        return self

    def angle_to(self, other: "Point") -> float:
        return math.atan2(other.y - self.y, other.x - self.x)

    def distance_to(self, other: "Point") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def __add__(self, other: Union["Point", int]) -> "Point":
        if isinstance(other, int):
            return Point(self.x + other, self.y + other)
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Union["Point", int]) -> "Point":
        if isinstance(other, int):
            return Point(self.x - other, self.y - other)
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int) -> "Point":
        return Point(self.x * other, self.y * other)

    def __truediv__(self, other: int) -> "Point":
        return Point(self.x / other, self.y / other)

    def __floordiv__(self, other: int) -> "Point":
        return Point(self.x // other, self.y // other)

    def __mod__(self, other: int) -> "Point":
        return Point(self.x % other, self.y % other)

    def __pow__(self, other: int) -> "Point":
        return Point(self.x**other, self.y**other)

    def __neg__(self) -> "Point":
        return Point(-self.x, -self.y)

    def __pos__(self) -> "Point":
        return Point(self.x, self.y)

    def __abs__(self) -> "Point":
        return Point(abs(self.x), abs(self.y))

    def __len__(self) -> int:
        return self.x + self.y

    def __eq__(self, other: "Point") -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: "Point") -> bool:
        return self.x != other.x or self.y != other.y

    def __lt__(self, other: "Point") -> bool:
        return self.x < other.x and self.y < other.y

    def __le__(self, other: "Point") -> bool:
        return self.x <= other.x and self.y <= other.y

    def __gt__(self, other: "Point") -> bool:
        return self.x > other.x and self.y > other.y

    def __ge__(self, other: "Point") -> bool:
        return self.x >= other.x and self.y >= other.y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"


class Path:

    def __init__(self):
        self.points: List[Point] = []
        self._index = 0
        return

    def add_point(self, point: Point):
        self.points.append(point)
        return

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self.points):
            point = self.points[self._index]
            self._index += 1
            return point
        raise StopIteration


class Line(Path):

    def __init__(self, start: Point, end: Point):
        super().__init__()
        self.p1 = start
        self.p2 = end
        self.points = self._calc_points()
        return

    """
    Uses Bresenham's Line Algorithm to calculate points on a line.
    """

    def _calc_points(self):
        points = []
        x1, y1 = self.p1.x, self.p1.y
        x2, y2 = self.p2.x, self.p2.y

        dx = abs(x2 - x1)
        dy = -abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx + dy

        while True:
            points.append(Point(x1, y1))
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x1 += sx
            if e2 <= dx:
                err += dx
                y1 += sy
        return points


class Triangle(Path):
    def __init__(self, p1: Point, p2: Point, p3: Point):
        super().__init__()
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.points = self._calc_points()
        return

    def _calc_points(self):
        line_one = Line(self.p1, self.p2)
        line_two = Line(self.p2, self.p3)
        line_three = Line(self.p3, self.p1)
        return line_one.points + line_two.points + line_three.points


class Rectangle(Path):
    def __init__(self, p1: Point, p2: Point, p3: Point, p4: Point):
        super().__init__()
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.points = self._calc_points()
        return

    def _calc_points(self):
        line_one = Line(self.p1, self.p2)
        line_two = Line(self.p2, self.p3)
        line_three = Line(self.p3, self.p4)
        line_four = Line(self.p4, self.p1)
        return line_one.points + line_two.points + line_three.points + line_four.points


class AnimationFrame:
    def __init__(self, start: Callable[[], None], stop: Callable[[], None]):
        self.start = start
        self.stop = stop
        return


class Graphics:
    def __init__(self):
        self._buffered_draw_calls: List[str] = []
        self._position: Point = Point(0, 0)
        return

    @staticmethod
    def reposition_cursor():
        print("\033[2J\033[H", end="")
        return

    @staticmethod
    def commit():
        sys.stdout.flush()
        return

    def begin_frame(self, reset_buffer: bool = True):
        if reset_buffer:
            self.reset_buffer()
        self.clear_screen()
        return

    def end_frame(self):
        Graphics.commit()
        Graphics.reposition_cursor()
        return

    def move(self, point: Point):
        y = max(1, point.y + 1)
        x = max(1, point.x + 1)
        self._buffered_draw_calls.append(f"\033[{y};{x}H")
        return self

    def draw(self, char: str):
        self._buffered_draw_calls.append(char)
        return self

    def translate(self, point: Point):
        self._position += point
        self._buffered_draw_calls.append(f"\033[{self._position.y};{self._position.x}H")
        return self

    def clear_screen(self):
        self._buffered_draw_calls.append("\033[2J\033[H")
        return self

    def reset_buffer(self):
        self._buffered_draw_calls = []
        return self

    def render(self):
        for draw_call in self._buffered_draw_calls:
            print(draw_call, end="")


class Animation:

    def request_frame(animatable: "Animatable", fps: int = 60):
        shared = {"thread": None, "should_run": True}

        def start():
            def loop():
                gfx: Graphics = animatable.ctx["gfx"]
                while shared["should_run"]:
                    gfx.begin_frame()
                    animatable.render()
                    gfx.end_frame()
                    time.sleep(1 / fps)

            thread = Thread(target=loop)
            thread.start()
            shared["thread"] = thread

        def stop():
            shared["should_run"] = False
            if shared["thread"] is not None:
                shared["thread"].join(timeout=1)

        return AnimationFrame(start, stop)

    class Animatable:
        def __init__(
            self, render_callback: Callable[[Dict[str, Any]], None] = None, **kwargs
        ):
            self._render_callback: Callable[[Dict[str, Any]], None] = render_callback
            self.ctx = kwargs | {"gfx": Graphics()}

        def render(self):
            self._render_callback(self.ctx)
            return


def option(name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__is_option_handler__ = True
        wrapper.__option_name__ = name
        return wrapper

    return decorator


def watch(*watch_names):
    def decorator(func):
        func.__is_watch_handler__ = True
        func.__watch_names__ = watch_names  # <--- attach to original function

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__is_watch_handler__ = True
        wrapper.__watch_names__ = watch_names
        return wrapper

    return decorator


def defer(*watch_names, debug_log: bool = False):
    def decorator(func):
        func.__is_defer_handler__ = True
        func.__watch_names__ = watch_names
        func.__debug_log__ = debug_log

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__is_defer_handler__ = True
        wrapper.__watch_names__ = watch_names
        wrapper.__debug_log__ = debug_log
        return wrapper

    return decorator


def readable(cls):
    def get_property(self):
        return self._readable

    def set_property(self, value):
        self._readable = value

    readable_property = property(get_property, set_property)

    setattr(cls, "_readable", True)
    setattr(cls, "readable", readable_property)

    return cls

def on_change(*watch_names):
    def decorator(func):
        # if func.__name__ == "on_change":
        #     func.__is_on_change_handler__ = True
        #     func.__watch_names__ = watch_names

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__is_on_change_handler__ = True
        wrapper.__watch_names__ = watch_names
        return wrapper

    return decorator

class DependencyGraph:
    def __init__(self):
        self._graph: Dict[str, List[Renderable]] = {}
        self._has_diffs = True
        return

    def build_deps(self, scene: "Scene"):
        for node in scene.nodes():
            # Try to get the on_change method
            method = getattr(node, "on_change", None)
            if not callable(method):
                continue
            # Unwrap method to get original function if it's bound
            func = getattr(method, "__func__", method)
            # Retrieve watch names from the decorator
            watch_names = getattr(func, "__watch_names__", None)
            if not watch_names:
                continue
            for name in watch_names:
                self.add_edge(node, name)
        Engine.debug(f"[dependency graph] build_deps() called: Dependency tree is: {self._graph}", trace=True)
        return

    def add_edge(self, node: "Renderable", dependency_key: str):
        if dependency_key not in self._graph:
            self._graph[dependency_key] = []
        if node._id in self._graph[dependency_key]:
            return
        self._graph[dependency_key].append(node)
        return

    def get_dependents_of(self, dependency_key: str) -> List["Renderable"]:
        return self._graph.get(dependency_key)

    def check_has_diffs(self):
        for dep in self._graph:
            for node in self._graph[dep]:
                if node.is_dirty():
                    return True
        return False

    def has_diffs(self):
        return self._has_diffs

    def _set_has_diffs(self, has_diffs: bool):
        self._has_diffs = has_diffs
        return


class DebugSnapshot:

    def __init__(self):
        self._dump: List[str] = [
            "=============== Snapshot started | time: " + self.timestamp() + "==============="
        ]
        return

    def timestamp(self):
        return time.strftime("%Y-%m-%d_%H-%M-%S")

    def _log(self, *args):
        return " ".join(args) + " | time: " + self.timestamp()

    def append(self, *args):
        for arg in args:
            self._dump.append(self._log(arg))
            self._dump.append("Logged at " + self.timestamp())
        return

    def write(self):
        self._dump.append(
            "=============== Snapshot ended | time: "
            + self.timestamp()
            + "==============="
        )
        with open(f"logs/snapshot-{self.timestamp()}.txt", "w") as f:
            f.write("\n".join(self._dump))
        return

class State:

    _engine: "Engine"

    def __init__(self, renderable: "Renderable", key: str, val: Any):
        if (self._engine._context.get(key)):
            self._engine._dependency_graph.add_edge(renderable, key)
        self._engine._context.set(key=val)
        return

    def update(self, key: str, val: Any):
        self._engine._context.set(key=val)
        return

class Context:
    def __init__(self, state: Dict[str, Any]):
        self.state = state
        return

    def bind(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return

    def get(self, *args):
        if len(args) == 1:
            Engine.debug(f"[context info] Getting value {args[0]} from context: {args[0]}", trace=True)
            return self.state.get(args[0])
        Engine.debug(f"[context info] Getting values {args} from context: {tuple(self.state.get(arg) for arg in args)}", trace=True)
        return tuple(self.state.get(arg) for arg in args)

    def set(self, **kwargs):
        diff_found = False
        for key, value in kwargs.items():
            if (self.state.get(key) == value):
                Engine.debug(f"[context info] no diff on value {key} is the same as {value} in context. The trace is: {''.join(traceback.format_stack())}")
                continue
            self.state[key] = value
            diff_found = True
            Engine.debug(f"[context info] diff found: {diff_found}")
            Engine.debug(f"[context info] ctx dump: {self.state}")
            dependents = Engine._dependency_graph.get_dependents_of(key)
            if not dependents:
                continue
            for dependent in dependents:
                Engine.debug(f"[ctx.set] notifying dependent: {dependent.__class__.__name__}, id: {id(dependent)}")
                method = getattr(dependent, "on_change", None)
                if not callable(method):
                    continue
                func = getattr(method, "__func__", method)
                watch_names = getattr(func, "__watch_names__", None)
                if not watch_names:
                    continue
                method(
                    *[self.state[name] for name in watch_names]
                )  # pass actual values
                dependent.mark_is_dirty()
        Engine._dependency_graph._set_has_diffs(diff_found)
        return kwargs

    def get_all(self):
        return self.state


# TODO
class Scene:

    _engine: "Engine"

    def __init__(self, nodes: List["Renderable"]):
        self._read_ptr = None
        self._nodes: List["Renderable"] = nodes
        # todo need to handle Groups here since they will effect the read pointer
        self._read_nodes = [node for node in nodes if isinstance(node, Readable)]
        if len(self._read_nodes) > 0:
            self._read_ptr = 0
        return

    def retry(self, node: "Renderable"):
        raise Exception("Not implemented")
        focus_index = self._read_nodes.index(node)
        if focus_index < 0:
            Engine.debug("[warn] Node not found in scene. Trace=scene.retry()")
            return
        # Debug
        self._read_ptr = focus_index
        Engine.debug(f"[info] Retrying node: {node._id}")
        node._did_render = False
        node.mark_is_dirty()
        node._did_process_response = False
        self._engine._dependency_graph._set_has_diffs(True)
        return

    def goto(self, node: "Renderable"):
        focus_index = self._nodes.index(node)
        if focus_index < 0:
            Engine.debug("[warn] Node not found in scene. Trace=scene.goto()")
            return
        self._read_ptr = focus_index
        return

    def on_tick(self, ctx: "Context", delta_time: float):
        Engine.debug(
            f"[scene info] Focused node: {self._read_nodes[self._read_ptr].name()}"
        )
        for node in self._nodes:
            node.on_tick(ctx, delta_time)
        return

    def after_render(self, ctx: "Context"):
        for node in self._nodes:
            node.after_render(ctx)
        return

    def before_render(self, ctx: "Context"):
        for node in self._nodes:
            node.before_render(ctx)
        return

    def nodes(self) -> List["Renderable"]:
        return self._nodes

    def _set_read_ptr(self, ptr: int):
        if ptr < 0 or ptr >= len(self._read_nodes):
            return
        self._read_ptr = ptr
        return

    def update_read_nodes(self, node: "Renderable", insert_index: int = None):
        if insert_index is None:
            self._read_nodes.append(node)
        else:
            self._read_nodes.insert(insert_index + 1, node)
        return

    def insert_node(
        self,
        node: "Renderable",
        as_child_of: "Renderable" = None,
        as_replacement_of: "Renderable" = None,
    ):
        if as_child_of:
            self._nodes.insert(self._nodes.index(as_child_of) + 1, node)
            if node.readable:
                self.update_read_nodes(node, self._nodes.index(as_child_of))
        elif as_replacement_of:
            self._nodes[self._nodes.index(as_replacement_of)] = node
            if node.readable:
                self.update_read_nodes(node, self._nodes.index(as_replacement_of))
                self._set_read_ptr(self._nodes.index(as_replacement_of))
        else:
            self._nodes.append(node)
            if node.readable:
                self.update_read_nodes(node)
        self._engine._events.emit("node_inserted", self.nodes())
        return self

    def _remove_read_node(self, node: "Readable"):
        index = self._read_nodes.index(node)
        if (index < self._read_ptr):
            self._read_ptr -= 1
        self._read_nodes.remove(node)
        return

    def delete_node(self, node: "Renderable"):
        if isinstance(node, Readable):
            self._remove_read_node(node)
        self._nodes.remove(node)
        self._engine._events.emit("node_deleted", self.nodes())
        return self

    def on_loaded(self):
        for node in self._nodes:
            node.on_start()
        return

    def on_will_transition(self):
        for node in self._nodes:
            node.on_end()
        return

    def on_input(self, input: str):
        if len(self._read_nodes) == 0:
            return
        if self._read_ptr + 1 > len(self._read_nodes):
            return
        if self._read_nodes[self._read_ptr]._has_option_handler() or isinstance(
            self._read_nodes[self._read_ptr], Selection
        ):
            self._read_nodes[self._read_ptr]._get_option_handler(input)
            self._read_nodes[self._read_ptr].did_process_response = True
        else:
            self._read_nodes[self._read_ptr].on_response(input)
            Engine.debug(f"[scene info] Processed input in scene.on_input() for {self._read_nodes[self._read_ptr].__class__.__name__}")
            self._read_nodes[self._read_ptr].did_process_response = True
        if not self._read_nodes[self._read_ptr].disabled:
            # if the receiver is not disabled, we should not increment the read pointer
            # assume it wants to keep the focus on the same node
            return
        self._set_read_ptr(self._read_ptr + 1)
        return


# TODO: Renderable
class Renderable:
    _engine: "Engine"
    _scene: Scene

    def __init__(
        self,
        disabled=False,
        hide_after_render=False,
        static=False,
        cached_render: Callable = None,
    ):
        self._id = str(uuid.uuid4())
        self.disabled = disabled
        self.hide_after_render = hide_after_render
        self.static = static
        self._is_dirty: bool = True
        self._did_render: bool = False
        if cached_render is not None:
            self.cached_render = cached_render
        return

    def name(self):
        return self.__class__.__name__

    def ctx(self):
        return Renderable._engine._context

    def on_tick(self, ctx: "Context", delta_time: float):
        return

    def did_render(self, ctx: "Context"):
        return

    def before_render(self, ctx: "Context"):
        return

    def after_render(self, ctx: "Context"):
        return

    def retry(self):
        Engine.debug("Retrying node: ", self._id, " - ", self.name())
        self._scene.retry(self)
        return

    def goto(self, node: "Renderable"):
        Engine.debug("Goto node: ", self._id, " - ", self.name())
        self._scene.goto(node)
        return

    def transition(self, scene_name: str):
        Engine.debug("Transitioning to scene: ", scene_name)
        self._engine.transition(scene_name)
        return

    def mark_is_dirty(self):

        self._is_dirty = True
        Engine.debug(f"Marking node {self.__class__.__name__} | id: {id(self)} as dirty", trace=True)
        Engine.debug()
        return

    def mark_clean(self):
        self._is_dirty = False
        Engine.debug(f"Marking node {self.__class__.__name__} | id: {id(self)} as clean", trace=True)
        return

    def is_dirty(self):
        return self._is_dirty

    def on_start(self):
        return

    def on_end(self):
        return

    def on_change(self, *args):
        return

    # base implementation does nothing
    def render(self) -> Callable[str, None]:
        return

    def cached_render(self) -> str:
        return f"{self.__class__.__name__} has not implemented cached_render()"

    def _has_option_handler(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and self._option_handler(attr):
                return True
        return False

    def _option_handler(self, method):
        return getattr(method, "__is_option_handler__", False)

    def _get_option_handler(self, result: str):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if (
                callable(attr)
                and self._option_handler(attr)
                and attr.__option_name__ == result
            ):
                return attr()
        Engine.debug(f"No handler found for option: {result}")
        return None

    def disable(self):
        self.disabled = True
        return

    def enable(self):
        self.disabled = False
        return

    def append_node(self, node: "Renderable"):
        self._scene.insert_node(node, as_child_of=self)
        self.mark_is_dirty()
        return self

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"""{self.__class__.__name__}(
        id={self._id},
        disabled={self.disabled},
        hide_after_render={self.hide_after_render},
        static={self.static},
        is_dirty={self._is_dirty},
        did_render={self._did_render}
        )"""

class Readable(Renderable):

    def __init__(self, static: bool = False, cached_render: Callable = None, hide_after_render: bool = False):
        self.readable = True
        self.did_process_response: bool = False
        super().__init__(static=static, cached_render=cached_render, hide_after_render=hide_after_render)
        return

    def on_response(self, response: str):
        return

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"""{self.__class__.__name__}(
        id={self._id},
        did_process_response={self.did_process_response},
        disabled={self.disabled},
        hide_after_render={self.hide_after_render},
        static={self.static},
        is_dirty={self._is_dirty},
        did_render={self._did_render}
        )"""

class Group(Renderable):
    def __init__(
        self,
        nodes: List["Renderable"],
        hide_after_render: bool = False,
        static: bool = False,
    ):
        self.nodes = nodes
        super().__init__(
            hide_after_render=hide_after_render, static=static
        )
        return

    def render(self):
        for node in self.nodes:
            node.render()
        return


class Text(Renderable):
    def __init__(self, text: str, static: bool = False):
        self.text = text
        super().__init__(static=static)
        return

    def render(self):
        return print(self.text)


class TypedText(Renderable):
    def __init__(
        self,
        text: str,
        speed: float = 0.05,
        hide_after_render: bool = False,
        static: bool = False,
    ):
        self.text = text
        self.speed = speed
        super().__init__(
            hide_after_render=hide_after_render, static=static
        )
        return

    def render(self):
        if self._did_render:
            if self.hide_after_render:
                return
            return print(self.text)
        self._did_render = True
        return utils.type_line(self.text, self.speed)


class TypedBlock(Renderable):
    def __init__(
        self,
        lines: List[str],
        speed: float = 0.05,
        hide_after_render: bool = False,
        static: bool = False,
    ):
        self.lines = lines
        self.speed = speed
        super().__init__(
            hide_after_render=hide_after_render, static=static
        )
        return

    def render(self):
        if self._did_render:
            if self.hide_after_render:
                return
            return print("\n".join(self.lines))
        return utils.type_text(self.lines, self.speed)


class Table(Renderable):
    def __init__(self, headers: List[str], rows: List[List[str]], static: bool = False):
        self.headers = headers
        self.rows = rows
        self._console = Console()
        super().__init__(static=static)
        return

    def render(self):
        table = RichTable(title="Table", expand=True)
        for col in self.headers:
            table.add_column(col, justify="right", style="cyan", no_wrap=True)
        for row in self.rows:
            if (
                self.highlight_row_no is not None
                and row == self.rows[self.highlight_row_no]
            ):
                table.add_row(*row, style="bold white on black")
            else:
                table.add_row(*row)
        return self._console.print(table)


class HighlightableTable(Table):
    def __init__(
        self,
        name: str,
        headers: List[str],
        rows: List[List[str]],
        static: bool = False,
    ):
        super().__init__(headers, rows, static=static)
        self.highlight_row_no: int = 0

    def on_start(self):
        self.highlight_row_no = HighlightableTable._engine._context.set(
            highlight_row_no=0
        )["highlight_row_no"]
        return

    def on_end(self):
        return

    @watch("highlight_row_no")
    def on_change(self, *args):
        self.highlight_row_no = args[0]
        return


class Question(Readable):

    def __init__(self, question: str, static: bool = False):
        self.question = question
        super().__init__(static=static)
        return

    def on_response(self, response: str):
        self.disable()
        return

    def render(self) -> str:
        return questionary.text(self.question).ask()


class Selection(Readable):
    def __init__(self, question: str, options: List[str], static: bool = False):
        self.question = question
        self.options = options
        super().__init__(static=static)
        return

    def render(self) -> List[str]:
        return questionary.select(self.question, choices=self.options).ask()


@dataclass
class RenderSanpshot:
    renderable: Renderable
    time: float
    was_rendered: bool


class RenderCache:
    def __init__(self):
        self._cache: Dict[str, RenderSanpshot] = {}
        return

    def cache(self, key: str, renderable: Renderable, was_rendered: bool = True):
        self._cache[key] = RenderSanpshot(renderable, time.time(), was_rendered)
        return

    def is_cached(self, renderable_id: str) -> bool:
        return renderable_id in self._cache

    def get(self, key: str) -> RenderSanpshot | None:
        return self._cache.get(key)


class Renderer:

    _tick_rate = 0.1
    _interrupted = False

    def __init__(self, engine: "Engine"):
        self._engine = engine
        self._buffer: List[Renderable] = []
        self._last_time = 0
        self._render_cache: RenderCache = RenderCache()
        self._render_pass_count = 0
        return

    def clear_buffer(self):
        self._buffer = []
        return

    def set_buffer(self, buffer: List[Renderable]):
        self._buffer = buffer
        return

    def clear_screen():
        if os.name == "nt":
            os.system("cls")
        else:
            print("\033[2J\033[H", end="")
        return

    def _should_defer(self, renderable: Renderable):
        # Look for a method decorated with @defer
        for attr_name in dir(renderable):
            attr = getattr(renderable, attr_name)
            if callable(attr) and getattr(attr, "__is_defer_handler__", False):
                show_log = getattr(attr, "__debug_log__", False)
                if show_log:
                    Engine.debug(f"Defer handler found for {attr_name}")
                required_keys = getattr(attr, "__watch_names__", [])
                for key in required_keys:
                    if (key not in self._engine._context.get_all()) or (
                        self._engine._context.get(key) is None
                    ):
                        return True
        return False

    # TODO Renderer
    def render(self):
        while True:
            Engine._interrupted = False
            delta_time = time.time() - self._last_time

            self._engine.get_current_scene().before_render(
                ctx=self._engine._context.get_all(),
            )

            # if not Engine._dependency_graph.has_diffs():
            #     Engine.debug("[render info] No diffs. Skipping render")
            #     self._engine.get_current_scene().on_tick(
            #         ctx=self._engine._context.get_all(),
            #         delta_time=delta_time,
            #     )
            #     sleep(self._tick_rate)
            #     continue

            Renderer.clear_screen()

            Engine.debug(f"[render info] Starting render pass {self._render_pass_count}")
            Engine.debug(
                f"[render info] Cleared screen at {time.time()}",
                f"[render info] Will render {len(self._buffer)} nodes",
                f"[render info] Nodes: {[node.__class__.__name__ for node in self._buffer]}",
                f"[render info] Node Info: {[node for node in self._buffer]}",
                new_lines=True,
            )

            for renderable in self._buffer:
                if (
                    renderable.disabled
                    or self._should_defer(renderable)
                ):
                    Engine.debug(
                        f"Renderable {renderable.__class__.__name__} is disabled or should defer"
                    )
                    continue

                if renderable._did_render and renderable.static:
                    if self._render_cache.get(renderable._id) is None:
                        self._render_cache.cache(renderable._id, renderable)
                    Engine.debug(f"[render info] Cached render for {renderable.__class__.__name__}")
                    print(self._render_cache.get(renderable._id).cached_render())
                    continue

                if isinstance(renderable, Readable) and not isinstance(renderable, Group):
                    if hasattr(renderable, "did_process_response") and renderable.did_process_response:
                        Engine.debug(f"[render info] Renderable {renderable.__class__.__name__} has already processed response. Passing on to next renderable")
                        continue
                    else:   
                        Engine.debug(f"[render info] Will process input for {renderable}")
                        resp = renderable.render()
                        self._engine._input_handler.process_input(resp)
                        renderable.did_process_response = True
                        self._render_cache.cache(renderable._id, renderable)
                else:
                    Engine.debug(f"[render info] Rendering {renderable.__class__.__name__}")
                    renderable.render()
                    self._render_cache.cache(renderable._id, renderable)

                if not renderable._did_render:
                    renderable.did_render(self._engine._context)

                renderable._did_render = True

                if renderable.hide_after_render:
                    self._engine.get_current_scene().delete_node(renderable)
                    Engine._dependency_graph._set_has_diffs(True)
                    Engine._interrupted = True
                    break

                renderable.mark_clean()

            self._last_time = time.time()
            self._engine.get_current_scene().on_tick(
                ctx=Engine._context,
                delta_time=delta_time,
            )

            if not Engine._interrupted:
                # if self._render_pass_count == 0:
                #     self._engine.get_current_scene().after_render(Engine._context)
                #     self._render_pass_count += 1
                Engine._dependency_graph._set_has_diffs(False)

            if self._render_pass_count == 0:
                for snap in self._render_cache._cache.values():
                    if snap.was_rendered:
                        Engine.debug(f"[render info] Calling after_render on: {snap.renderable.__class__.__name__} in render pass {self._render_pass_count}")
                        snap.renderable.after_render(Engine._context)

            self._render_pass_count += 1
            sleep(self._tick_rate)


class InputHandler:
    def __init__(self, engine: "Engine"):
        self._engine = engine
        return

    def process_input(self, input: str):
        self._engine.get_current_scene().on_input(input)
        return


class Events:

    def __init__(self):
        self._events: Dict[str, List[Callable[[Any], None]]] = {}
        return

    def on(self, event: str, callback: Callable[[Any], None]):
        if event not in self._events:
            self._events[event] = []
        self._events[event].append(callback)
        return

    def emit(self, event: str, *args, **kwargs):
        if event not in self._events:
            return
        for callback in self._events[event]:
            callback(*args, **kwargs)
        return


class Engine:

    _context: Context = Context({})
    _dependency_graph: DependencyGraph = DependencyGraph()
    _events: Events = Events()
    _snapshot: DebugSnapshot = DebugSnapshot()
    DEBUG_MODE: bool = False
    DEBUG_SILENT: bool = True

    def __init__(self, debug_mode: bool = False, debug_silent: bool = True):
        Engine.DEBUG_MODE = debug_mode
        Engine.DEBUG_SILENT = debug_silent
        self.scenes: Dict[str, Scene] = {}
        self._renderer = Renderer(self)
        self._render_thread = Thread(target=self._renderer.render)
        self._current_scene: Scene = None
        self._input_handler: InputHandler = InputHandler(self)
        return

    def set_debug_mode(self, debug_mode: bool, silent: bool = False):
        self.DEBUG_MODE = debug_mode
        self.DEBUG_SILENT = silent
        return

    def debug(
        *args,
        on_new_lines: bool = False,
        fg: utils.ForegroundColor = utils.ForegroundColor.Black,
        bg: utils.BackgroundColor = utils.BackgroundColor.White,
        trace: bool = False,
        **kwargs,
    ):
        if Engine.DEBUG_MODE:
            _time = time.strftime("%Y-%m-%d_%H-%M-%S")
            frame = inspect.currentframe().f_back
            context_info = inspect.getframeinfo(frame)
            context_details = f"Trace: {context_info.function} in {context_info.filename} at line {context_info.lineno} | time: {_time}"
            
            if not on_new_lines and not args and not kwargs:
                if not Engine.DEBUG_SILENT:
                    utils.debug_log(context_details, fg=fg, bg=bg)
                Engine._snapshot.append(context_details)
                return
            if on_new_lines:
                if not Engine.DEBUG_SILENT:
                    utils.debug_log("\n".join(map(str, args)) + f" | trace: {context_details}", fg=fg, bg=bg)
                Engine._snapshot.append("\n".join(map(str, args)) + " | trace: " + context_details)
            else:
                if not Engine.DEBUG_SILENT:
                    utils.debug_log(".".join(map(str, args)) + f" | trace: {context_details}", fg=fg, bg=bg)
                Engine._snapshot.append(".".join(map(str, args)) + " | trace: " + context_details)
        return

    def set_context(context: Dict[str, Any]):
        Engine._context.set(**context)
        return

    def transition(self, scene: str):
        self._renderer.clear_buffer()
        if self._current_scene:
            self._current_scene.on_will_transition()
        self._current_scene = self.scenes[scene]
        self._dependency_graph.build_deps(self._current_scene)
        self._renderer.set_buffer(self._current_scene.nodes())
        Renderable._engine = self
        Renderable._scene = self._current_scene
        Renderable._engine._context = self._context
        self._current_scene._engine = self

        self._current_scene.on_loaded()
        return

    def add_scenes(self, scenes: Dict[str, Scene], initial_scene: str = None):
        self.scenes = scenes
        if len(self.scenes) == 0:
            raise Exception("No scenes added")
        if initial_scene:
            self.transition(initial_scene)
        else:
            self.transition(list(self.scenes.keys())[0])
        return

    def _on_node_inserted(self, nodes: List[Renderable]):
        Engine.debug("[event] node_inserted received.. nodes at time of resset are ", nodes)
        self._renderer.set_buffer(nodes)
        self._dependency_graph.build_deps(self._current_scene)
        self._dependency_graph._set_has_diffs(True)
        return

    def _on_node_deleted(self, nodes: List[Renderable]):
        self._renderer.set_buffer(nodes)
        self._dependency_graph._set_has_diffs(True)
        return

    def _on_node_changed(self, nodes: List[Renderable]):
        self._renderer.set_buffer(nodes)
        self._dependency_graph._set_has_diffs(True)
        return

    def on_exit(self):
        Engine._snapshot.write()
        return

    def start(self):
        Engine._events.on("node_inserted", self._on_node_inserted)
        Engine._events.on("node_deleted", self._on_node_deleted)
        Engine._events.on("node_changed", self._on_node_changed)

        atexit.register(self.on_exit)

        self._render_thread.start()
        return

    def stop(self):
        self._render_thread.join()
        return

    def safe_exit(self, failed: bool = False):
        self._render_thread.join()
        if failed:
            sys.exit(1)
        sys.exit(0)

    def exit(failed: bool = False):
        if failed:
            sys.exit(1)
        sys.exit(0)

    def get_current_scene(self):
        return self._current_scene


class ColorSelector(Selection):
    def __init__(self, question: str):
        super().__init__(question, ["Red", "Blue", "Green"])
        return

    @option("Red")
    def option_one(self):
        ColorSelector._engine._context.set(highlight_row_no=0)
        return

    @option("Blue")
    def option_two(self):
        ColorSelector._engine._context.set(highlight_row_no=1)
        return

    @option("Green")
    def option_three(self):
        ColorSelector._engine._context.set(highlight_row_no=2)
        return


class NameQuestion(Question):
    def on_response(self, response: str):
        self.disable()
        return


class SceneTwo(Scene):
    def render(self) -> List[str]:
        return ["Scene Two"]


# def test():
#     engine = Engine()
#     Engine.set_context(
#         {
#             "highlight_row_no": 0,
#             "tracks": [
#                 {"name": "Fly Me To The Moon", "duration": "1h"},
#                 {"name": "I Will Always Love You", "duration": "2h"},
#                 {"name": "Don't Stop Believin'", "duration": "3h"},
#             ],
#         }
#     )
#     engine.add_scenes(
#         {
#             "scene_one": Scene(
#                 [
#                     HighlightableTable(
#                         "tracks_table",
#                         ["Track", "Duration"],
#                         [
#                             ["Fly Me To The Moon", "1h"],
#                             ["I Will Always Love You", "2h"],
#                             ["Don't Stop Believin'", "3h"],
#                         ],
#                     ),
#                     TypedText("Hi, welcome to grandor!"),
#                     NameQuestion("What is your name?"),
#                     ColorSelector("What is your favorite color?"),
#                 ]
#             )
#         }
#     )
#     engine.start()


# ## anytime data changes on the scene, just redraw the entire terminal
