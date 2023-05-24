from manim import *
from numpy import sin  # for sin plot


config.background_color = "#0c0b29"
config.pixel_height = 1080
config.pixel_width = 1920


class TwoDPlot(Scene):
    def construct(self):
        # make content
        plane = NumberPlane(x_range=(-9, 9), y_range=(-9, 9))
        ax = Axes(x_range=(-3, 3), y_range=(-3, 3))
        ax.color = ORANGE
        curve = ax.plot(lambda x: sin(x), color=RED)

        # curve.set_color_by_gradient("#00d4ff", "#090979")
        # curve.set_sheen_direction(RIGHT)

        # play content
        self.add(plane)
        self.play(Create(ax, run_time=2), Create(curve, run_time=3))
        self.play(Indicate(curve))
