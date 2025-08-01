import math
import random
from typing import Any, Callable, Dict, List, Union
import sys
import time
from threading import Thread


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
