from simple_renderer import Engine, Graphics, Point, Line, Rectangle, Animation
from scenes.home.scene import Home
import math
import time
from utils import debug_log

# def line():
#     gfx = Graphics()
#     line = Line(Point.origin(), Point(1, 12))
#     for point in line:
#         # print(point)
#         gfx.move(point).draw("*")
#     gfx.render()


# def sine_wave():
#     Graphics.reposition_cursor()
#     gfx = Graphics()

#     width = 100
#     amplitude = 8
#     vertical_offset = 8

#     for x in range(width):
#         gfx.reset_buffer()

#         # Compute y based on sine wave
#         y = vertical_offset + int(
#             amplitude * math.sin(x * 0.2)
#         )  # scale x for better frequency
#         point = Point(x, y)

#         gfx.clear_screen()  # clear terminal screen
#         gfx.move(point).draw("*")
#         gfx.render()
#         Graphics.commit()
#         time.sleep(0.05)


# def animated_sine_wave():
#     Graphics.reposition_cursor()
#     gfx = Graphics()

#     width = 80  # Terminal width in characters
#     amplitude = 8  # How tall the wave is
#     offset_y = 10  # Vertical center line
#     speed = 0.2  # Phase shift speed
#     scale_x = 0.3  # Horizontal stretching

#     phase = 0  # Time-based phase shift

#     while True:
#         gfx.clear_screen()
#         gfx.reset_buffer()

#         for x in range(width):
#             y = offset_y + int(amplitude * math.sin(scale_x * x + phase))
#             gfx.move(Point(x, y)).draw("*")

#         gfx.render()
#         Graphics.commit()
#         Graphics.reposition_cursor()
#         time.sleep(0.001)

#         phase += speed  # shift wave to the left


# def request_anim_test():
#     def render_animated_sine_wave(ctx):
#         for x in range(ctx["width"]):
#             y = ctx["offset_y"] + int(
#                 ctx["amplitude"] * math.sin(ctx["scale_x"] * x + ctx["phase"])
#             )
#             ctx["gfx"].move(Point(x, y)).draw("*")
#         ctx["gfx"].render()
#         ctx["phase"] += ctx["speed"]

#     swave = Animation.Animatable(
#         render_animated_sine_wave,
#         width=80,
#         amplitude=8,
#         offset_y=10,
#         speed=0.2,
#         scale_x=0.3,
#         phase=0,
#     )

#     anim_block = Animation.request_frame(swave)
#     anim_block.start()
#     time.sleep(5)
#     anim_block.stop()
#     print("Animation finished")


# def random_falling_star():
#     Graphics.reposition_cursor()
#     gfx = Graphics()

#     start_height = 15
#     current_pos = Point.origin()
#     for i in range(10):
#         gfx.move(current_pos).draw("⭐️").render()
#         current_pos += Point.rand_point(start_height - i)
#         gfx.reset_buffer()
#         gfx.clear_screen()
#         Graphics.commit()
#         time.sleep(0.8)


# def rect():
#     gfx = Graphics()
#     rect = Rectangle(Point(0, 0), Point(0, 20), Point(10, 20), Point(10, 0))
#     gfx.begin_frame(reset_buffer=False)
#     while True:
#         for point in rect:
#             gfx.move(point).draw("*")
#             gfx.render()
#             gfx.end_frame()
#             time.sleep(0.1)


def init():

    # session = Session()
    # session.start()

    # session.graphics.display_boot()
    # session.io.write(
    #     messages["start_prompt"],
    #     OutputType.question,
    #     lambda response: session.events.emit(SessionEvents.file_dropped, response),
    # )

    # test()


    engine = Engine(debug_mode=True, debug_silent=False)
    engine.add_scenes({
        "home": Home,
    })
    engine.start()

    # while True:
    #     time.sleep(0.1)

    # gfx = Graphics()
    # line = Line(Point.origin(), Point(12, 12))
    # for point in line:
    #     gfx.move(point).draw("*")
    # gfx.render()

    return


if __name__ == "__main__":

    init()
    # try:
    #     # sine_wave()
    #     # random_falling_star()
    #     # line()
    #     # animated_sine_wave()
    #     # request_anim_test()

    #     # rect()
    #     # animated_sine_wave()
    #     # time.sleep(0.1)

    #     init()

    # except KeyboardInterrupt:
    #     pass
    # except Exception as e:
    #     print(e)
