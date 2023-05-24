from manim import *


class angle(Scene):
    def construct(self):
        line1 = Line(ORIGIN, RIGHT, color=BLUE)
        line2 = Line(ORIGIN, RIGHT, color=RED)
        line3 = Line(line1.start, line1.end + (UP * 2), color=PURPLE)
        print(f"line3 ends at: {line3.end}")
        line3.end += UP * 0.001

        angol = Angle(line2, line3, 0.5, color=YELLOW)
        self.add(line2)
        # self.add(line3)
        self.add(angol)

        # comparison = line1.end != line2.end
        # print(f"Lines r NOT parallel: {(line1.end != line2.end).all()}")
        # if (line2.start, line1.end) != (line2.start, line2.end):
