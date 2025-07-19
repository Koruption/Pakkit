from ast import Dict
import uuid
from abc import abstractmethod
from functools import wraps
from typing import List, Any, Dict, TYPE_CHECKING
import inspect
import time
from threading import Thread
import sys
from dataclasses import dataclass


def option(name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__is_option_handler__ = True
        wrapper.__option_name__ = name
        return wrapper

    return decorator

# def engine_callable():
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             # Get the calling frame
#             frame = inspect.currentframe().f_back
#             caller_self = frame.f_locals.get("self", None)
#             print("Caller self: ", caller_self)

#             allowed_types = (Engine, EngineContext, Renderer, InputHandler)

#             if isinstance(caller_self, allowed_types):
#                 return func(*args, **kwargs)
#             else:
#                 raise Exception(
#                     f"'{func.__qualname__}' is an engine-only method and was called from '{type(caller_self).__name__}' context"
#                 )

#         return wrapper

#     return decorator


class RenderNode:
    readable: bool = False

    def __init__(self):
        self._is_dirty: bool = True
        self._id = uuid.uuid4()
        return

    def render(self, ctx: "EngineContext") -> str:
        return ""

    def mark_is_dirty(self):
        self._is_dirty = True
        return

    def mark_clean(self):
        self._is_dirty = False
        return

    def is_dirty(self):
        return self._is_dirty

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
        return None

    def on_input(self, input: str):
        return


class DependencyGraph:

    def __init__(self):
        # keys map to ctx instances and values map to lists of nodes that depend on the ctx instance
        self._graph: Dict[str, List[str]] = {}
        return

    def add_edge(self, node: RenderNode, dependency_key: str):
        if dependency_key not in self._graph:
            self._graph[dependency_key] = []
        if node._id in self._graph[dependency_key]:
            return
        self._graph[dependency_key].append(node._id)
        return

    def get_dependents_of(self, dependency_key: str) -> List[RenderNode]:
        return self._graph[dependency_key]


class EngineContext:

    _engine_schemas: Dict[str, Any] = {}
    dep_tree: DependencyGraph = DependencyGraph()

    def add_schema(name: str, schema: Dict[str, Any]):
        if name in EngineContext._engine_schemas:
            EngineContext._engine_schemas[name] = EngineContext._engine_schemas[name] | schema
            return
        EngineContext._engine_schemas[name] = schema
        return

    def update(dispatcher: RenderNode, name: str, patch: Dict[str, Any]):
        for k, v in patch.items():
            EngineContext._engine_schemas[name][k] = v
        # TODO: Implement the rest of this i.e., add to dep_tree methods
        [node.mark_is_dirty() for node in EngineContext.dep_tree.dependents_of(name)]
        return

    def read(reader: RenderNode, name: str):
        EngineContext.dep_tree.add_edge(reader, name)
        return EngineContext._engine_schemas[name]


class Scene:
    def __init__(self):
        self._read_ptr = 0
        self._nodes: List[RenderNode] = (
            []
        )  # this is set by the engine in the render method
        return

    # @engine_callable()
    def render(self, ctx: EngineContext) -> List[RenderNode]:
        return []

    # engine_callable() will be a decorator that throws if a non Engine scope calls it
    # subclasses should NOT override this method
    # @engine_callable()
    def _on_input(self, input: str):
        focused_node = self._nodes[self._read_ptr]
        if focused_node._has_option_handler():
            # render node is an option node
            # call the corresponding option handler
            focused_node._get_option_handler(input)
        else:
            focused_node.on_input(input)
        self._read_ptr += 1
        return

    def update(self, ctx: EngineContext):
        return

    # called by the engine
    # @engine_callable()
    def _set_nodes(self, nodes: List[RenderNode]):
        self._nodes = [node for node in nodes if node.readable]
        return

    # @engine_callable()
    def _get_nodes(self):
        return self._nodes

    # @engine_callable()
    def _get_read_ptr(self):
        return self._read_ptr


class Selection(RenderNode):

    def __init__(self, options: List[str]):
        self.options = options
        return

    def render(self) -> str:
        return ""


# class AnimeSelection(Selection):
#     def __init__(self):
#         super().__init__(
#             [
#                 "Attack on Titan",
#                 "One Piece",
#                 "Naruto",
#             ]
#         )
#         self.anim_selection = ctx(
#             "anim_selection", {"txt": "What's your favorite anime?"}
#         )
#         return

#     def render(self) -> str:
#         return read("anim_selection")

#     @option("Attack on Titan")
#     def on_attack_on_titan(self):
#         update("anim_selection", {"txt": "Attack on Titan"})
#         return

# class PlaybackScene(Scene):
#     def __init__(self):
#         return

#     def render(self, ctx: EngineContext) -> List[RenderNode]:
#         return [
#             Table(["Track", "Duration"], [[ctx.current_track, ctx.track_duration]]),
#             ProgressBar(progress=ctx.track_progress),
#             Selection(
#                 "Controls: Play/Pause, Next, Previous, Exit, Volume Up, Volume Down"
#             ),
#         ]

#     def on_input(self, input: str):
#         return

#     @option("Play/Pause")
#     def on_play_pause(self, option: str):
#         return

#     @option("Next")
#     def on_next(self, option: str):
#         self.update({"current_track": self.current_track + 1})
#         return

#     @option("Previous")
#     def on_previous(self, option: str):
#         self.update({"current_track": self.current_track - 1})
#         return

#     @option("Exit")
#     def on_exit(self, option: str):
#         Engine.transition("home")
#         return

#     @option("Volume Up")
#     def on_volume_up(self, option: str):
#         return

#     @option("Volume Down")
#     def on_volume_down(self, option: str):
#         return


class InputHandler:

    def __init__(self):
        self._input_buffer: List[str] = []
        return

    def get_input(self):
        if not self._input_buffer:
            return None
        return self._input_buffer.pop(0)

    def listen(self):
        while True:
            try:
                io = input("> ").strip()
                if not io:
                    continue
                if io.lower() == "q":
                    print("Exiting...")
                    sys.exit(0)
                # dispatch input to current scene
                Engine.get_current_scene()._on_input(io)
                self._input_buffer.append(io)
            except EOFError:
                break
            except KeyboardInterrupt:
                print("\nInterrupted.")
                sys.exit(0)
        return


@dataclass
class RenderNodeTarget:
    node: RenderNode
    start_line: int
    offset: int


class Renderer:

    def __init__(self):
        self._buffer: List[RenderNodeTarget] = []
        return

    def calc_lines(node: RenderNode):
        return len(node.render(Engine._ctx).split("\n"))

    def get_lines(node: RenderNode):
        return node.render(Engine._ctx).split("\n")

    def buffer_line_count(self):
        return sum([node.offset for node in self._buffer])

    def buffer(self, node: RenderNode):
        self._buffer.append(
            RenderNodeTarget(
                node=node,
                start_line=self.buffer_line_count(),
                offset=Renderer.calc_lines(node),
            )
        )
        return

    def fill_scene_buffer(self, scene: Scene):
        if len(self._buffer) > 0:
            raise Exception("Buffer is not empty. Call clear_buffer() first.")
        for node in scene._get_nodes():
            self.buffer(node)
        return

    def clear_buffer(self):
        self._buffer = []
        return

    def move_to_line(self, line: int):
        for node in self._buffer:
            if node.start_line <= line < node.start_line + node.offset:
                return node
        return None

    def _update_start_lines(self, start_indx, end_indx, line_offset):
        for i in range(start_indx, end_indx):
            self._buffer[i].start_line += line_offset
        return

    def render(self):
        Engine.get_current_scene()._set_nodes(Engine.get_current_scene().render(Engine._ctx))
        while True:
            if not self._buffer:
                continue
            for index, node in enumerate(self._buffer):
                if node.node.is_dirty():
                    if (
                        node.node.readable
                        and Engine.get_current_scene()._get_read_ptr() != index
                    ):
                        continue
                    new_offset = Renderer.calc_lines(node.node)
                    if new_offset != node.offset:
                        node.offset = new_offset
                        self.move_to_line(node.start_line)
                        print(node.node.render(Engine._ctx))
                        node.node.mark_clean()
                        self._update_start_lines(
                            index, len(self._buffer), new_offset - node.offset
                        )
                        node.node.mark_clean()
                        continue 
                    print(node.node.render(Engine._ctx))
                    node.node.mark_clean()
                # implement later
                time.sleep(0.1)


class Engine:
    current_scene: str = None
    _renderer: Renderer = Renderer()
    _scheduled_updates: List[{"node": RenderNode, "patch": Dict[str, Any]}] = []
    _scenes: Dict[str, Scene] = {}
    _ctx: "EngineContext" = EngineContext()
    _rendering_thread: Thread = None
    _input_thread: Thread = None
    _input_handler: InputHandler = InputHandler()

    def __init__(self):
        return

    def transition(scene: str):
        Engine._renderer.clear_buffer()
        Engine.current_scene = scene
        Engine.get_current_scene()._set_nodes(Engine.get_current_scene().render(Engine._ctx))
        Engine._renderer.fill_scene_buffer(Engine.get_current_scene())
        return

    def register_scenes(scenes: Dict[str, Scene]):
        Engine._scenes = scenes
        return

    def get_current_scene() -> Scene:
        if not Engine.current_scene:
            raise Exception("No current scene")
        return Engine._scenes[Engine.current_scene]

    def run():
        # listen for scene changes at the top level
        if not Engine.current_scene:
            Engine.current_scene = list(Engine.scenes.keys())[0]
        # this runs indefinitely
        Engine._rendering_thread = Thread(target=Engine._renderer.render)
        Engine._input_thread = Thread(target=Engine._input_handler.listen)
        Engine._input_thread.start()
        Engine._rendering_thread.start()

    def stop():
        Engine._rendering_thread.join()
        Engine._input_thread.join()
        return

    def queue_update(node: RenderNode):
        # TODO: FINISH THIS 
        Engine._scheduled_updates.append({"node": node, "patch": {}})
        return


# global update function
def update(name: str, patch: Dict[str, Any]):
    # Get the previous frame in the call stack
    frame = inspect.currentframe().f_back

    # Get the 'self' object if this was a method call
    caller_self = frame.f_locals.get("self", None)
    if caller_self:
        EngineContext.update(caller_self, name, patch)
    else:
        raise Exception("Update called from non-method context")
    return


# global read function for reading engine ctx values
def read(name: str):
    # Get the previous frame in the call stack
    frame = inspect.currentframe().f_back

    # Get the 'self' object if this was a method call
    caller_self = frame.f_locals.get("self", None)
    if caller_self:
        return EngineContext.read(caller_self, name)
    else:
        raise Exception("Ctx called from non-method context")


# global ctx function
def ctx(name: str, state: Dict[str, Any], subscribe: bool = False):
    # Get the previous frame in the call stack
    frame = inspect.currentframe().f_back

    # Get the 'self' object if this was a method call
    caller_self = frame.f_locals.get("self", None)
    if caller_self:
        EngineContext.add_schema(name, state)
        if subscribe:
            EngineContext.dep_tree.add_edge(caller_self, name)
    else:
        raise Exception("Ctx called from non-method context")


# engine = Engine()
# engine.register_scenes(
#     {
#         "scene_1": HomeScene,
#         "scene_2": PlaybackScene,
#         "scene_3": PruningScene,
#     }
# )
# engine.run()


"""
- When ctx.update() is called, the engine should determine who called the update
- When this happens, we need to mark that ctx value as a dependency of the node
- When the node is re-rendered, it should check if any of its dependencies have changed
- If any of its dependencies have changed, it should re-render
- If none of its dependencies have changed, it should skip re-rendering
- When the node is re-rendered, it should update the buffer
"""


# =============== TEST CODE ===============
class WelcomeNode(RenderNode):
    readable = True

    def __init__(self):
        super().__init__()
        ctx("welcome_msg", {"text": "🎮 Welcome to NeraPakker CLI!"})

    def render(self, ctx: EngineContext) -> str:
        return read("welcome_msg")["text"]


class ContinueSelection(RenderNode):
    readable = True

    def __init__(self):
        super().__init__()
        ctx("continue_prompt", {"text": "\nType 'Continue' to start, or 'q' to quit."})

    def render(self, ctx: EngineContext) -> str:
        return read("continue_prompt")["text"]

    @option("Continue")
    def on_continue(self):
        update("continue_prompt", {"text": "Loading scene..."})
        time.sleep(0.5)
        Engine.transition("scene_2")


class HomeScene(Scene):
    def render(self, ctx: EngineContext) -> List[RenderNode]:
        return [WelcomeNode(), ContinueSelection()]


class PlaybackScene(Scene):
    def render(self, ctx: EngineContext) -> List[RenderNode]:
        return [StaticMessage("You’re now in the PlaybackScene. Type 'q' to quit.")]


class StaticMessage(RenderNode):
    readable = True

    def __init__(self, msg: str):
        super().__init__()
        self.msg = msg

    def render(self, ctx: EngineContext) -> str:
        return self.msg


def test():
    Engine.register_scenes(
        {
            "scene_1": HomeScene(),
            "scene_2": PlaybackScene(),
            # Optional placeholder scene for expansion
            "scene_3": Scene(),
        }
    )
    Engine.transition("scene_1")
    Engine.run()
