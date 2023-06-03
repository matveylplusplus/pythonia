from manim import *


class CreateCircle(Scene):
    def construct(self):
        self.camera.background_color = "#1d3461"
        circle = Circle()  # create a circle!
        circle.color = YELLOW
        circle.set_fill(RED, opacity=1)  # set color and transparency
        self.play(Create(circle))  # show the circle on screen


class DifferentRotations(Scene):
    def construct(self):
        left_square = Square(color=BLUE, fill_opacity=0.7).shift(3 * LEFT)
        right_square = Square(color=GREEN, fill_opacity=0.7).shift(3 * RIGHT)
        left_square.rotate_about_origin(-(3 * PI) / 2)
        self.play(
            left_square.animate.rotate_about_origin((3 * PI) / 2),
            Rotate(right_square, angle=PI),
            run_time=2,
        )
        self.wait()
