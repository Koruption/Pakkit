import questionary
from typing import List, Callable, Any, Dict, Optional, Union
import utils
from uuid import uuid4


class Renderable:

    def __init__(
        self,
        render_once=False,
        defer_render=False,
        cacheable=False,
        render: Callable[[], None] = None,
        cache_val: str = None,
    ):
        self.id = str(uuid4())
        self.render_once = render_once
        self.defer_render = defer_render
        self.cacheable = cacheable if not render_once else False
        self.should_remove = False
        self.did_start = False
        self._render = render
        self._cache_val = cache_val
        self._post_render_callbacks: List[
            Callable[[Union["Renderable", None]], None]
        ] = []
        return

    def on_start(self):
        return

    def on_tick(self, delta_time: float):
        return

    def on_end(self):
        return

    def render(self) -> None:
        if self._render:
            return self._render()
        raise NotImplementedError()

    def post_render(self):
        for callback in self._post_render_callbacks:
            callback(self)
        return

    def render_cached(self) -> str:
        if self._cache_val:
            return self._cache_val
        raise NotImplementedError()

    def should_use_cache(self):
        return self.did_start and not self.render_once and self.cacheable

    def mark_for_removal(self):
        self.should_remove = True

    def then(self, callback: Callable[["Renderable"], None]):
        self._post_render_callbacks.append(callback)
        return self


class Text(Renderable):

    def __init__(
        self,
        text: str,
        render_once=False,
        defer_render=False,
    ):
        self.text = text
        super().__init__(render_once, defer_render, cacheable=True, cache_val=self.text)

    def render(self):
        return print(self.text)


class Readable(Renderable):

    def __init__(self, render_once: bool = True, defer_render: bool = False):
        self.redirects: Dict[str, List[Renderable]] = {}
        super().__init__(
            render_once=render_once, defer_render=defer_render, cacheable=False
        )

    # this can be overriden for more custom/controllable
    # conditional renders
    def on_response(
        self, response: str
    ) -> Optional[Union[List[Renderable], Renderable]]:
        for key, renderables in self.redirects.items():
            if key == response:
                return renderables
        return

    def on(self, redirects: Dict[str, Union[Renderable, List[Renderable]]]):
        if not isinstance(redirects, dict):
            raise Exception("Redirects must be of type dict.")
        for key, val in redirects.items():
            if not isinstance(val, list):
                redirects[key] = [val]
        if self.redirects:
            self.redirects = self.redirects | redirects
            return self
        self.redirects = redirects
        return self


class TypedText(Renderable):

    def __init__(
        self,
        text: str,
        delay: float = 0.04,
    ):
        self.text = text
        self.delay = delay
        super().__init__(render_once=True)

    def render(self):
        return utils.type_line(self.text, self.delay)


class Question(Readable):

    def __init__(self, prompt: str, render_once=True, defer_render=False):
        self.prompt = prompt
        super().__init__(render_once=render_once, defer_render=defer_render)

    def render(self):
        return questionary.text(self.prompt).ask()


class Selection(Readable):

    def __init__(
        self, prompt: str, choices: List[str], render_once=True, defer_render=False
    ):
        self.prompt = prompt
        self.choices = choices
        super().__init__(render_once=render_once, defer_render=defer_render)

    def render(self):
        return questionary.select(self.prompt, choices=self.choices).ask()
