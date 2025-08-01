from core.primitives import Animatable
from core.primitives import Question, Selection, TypedText
from core.engine import Engine, Scene


def init():
    engine = Engine()
    engine.scenes.define(
        {
            "home": Scene(
                [
                    TypedText("Hello, welcome home!", delay=1),
                    Animatable(fps=60, defer_render=False).alloc(15),
                    Question("What's your favorite music genre?").on(
                        {
                            "metal": Selection(
                                "Favorite sub-genre?",
                                choices=["djent", "black", "power"],
                            ),
                            "pop": [
                                TypedText("Are you serious?! Pop Sucks!", 0.02),
                                Question("Tell me what you like about pop lol").on(
                                    {"": TypedText("Odd, I hate pop")}
                                ),
                            ],
                        }
                    ),
                    TypedText("This is the end.. my only friend, the end..").then(
                        lambda renderable: print(
                            f"Goodbye... from {renderable.__class__.__name__}"
                        )
                    ),
                ]
            ),
            "playback": Scene([TypedText("Welcome to the playback scene!")]),
        }
    )
    engine.start()
    return


if __name__ == "__main__":
    init()