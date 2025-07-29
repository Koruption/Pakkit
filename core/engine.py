from typing import List, Dict, OrderedDict
from core.io import InputStream
from core.diffing import DiffEngine
from core.primitives import Renderable
from core.events import EngineEvents
from core.renderer import Renderer


class Scene:

    def __init__(self, layout: List[Renderable]):
        self.layout = layout


class SceneManager:

    def __init__(self, renderer: Renderer):
        self.graph: Dict[str, Scene] = {}
        self.renderer = renderer
        self.focused: Renderable = None
        self.current: str = None
        return

    def define(
        self, graph: OrderedDict[str, Scene], start_scene: str = None
    ) -> List[Renderable]:
        self.graph = graph
        if not start_scene:
            self.current = list(graph.keys())[0]
        else:
            self.current = start_scene
        return  # stub

    def get_scene(self, name: str):
        return self.graph.get(name)

    def transition(self, name: str):
        if name not in self.graph:
            raise Exception(f"Name: {name}, not registered in scene graph.")
        self.renderer.set_buffer(self.graph[name])

    def mark_focused(self, renderable: Renderable):
        self.focused = renderable


class Engine:

    def __init__(self):
        self.events: EngineEvents = EngineEvents()
        self.scenes = SceneManager(self.events)
        self.diffing = DiffEngine()
        self.renderer = Renderer(self.events, self.diffing)
        self.render_thread = self.renderer.get_thread()
        self.io = InputStream()
        return
    
    def cursor_watch(self):
        return 

    def start(self):
        self.renderer.set_buffer(self.scenes.get_scene(self.scenes.current).layout)
        self.render_thread.start()
        self.io.start()

    def stop(self):
        self.render_thread.join()
        self.io.stop()
