from manim import *


class CircleChordAnimation(Scene):
    def construct(self):
        # Generate a circle
        circle = Circle(radius=2)
        self.play(Create(circle))

        # Form two lines protruding from the center
        line1 = Line(start=circle.get_center(), end=circle.point_from_proportion(0.4))
        line2 = Line(start=circle.get_center(), end=circle.point_from_proportion(0.8))
        self.play(Create(line1), Create(line2))

        # Create the chord line between the two lines
        chord = Line(start=line1.get_end(), end=line2.get_end())
        self.play(Create(chord))

        # Animate the angle and drag one of the lines
        angle = Angle(line1, line2, radius=0.5)
        self.play(Create(angle))

        def update_angle_and_drag_line(mob, alpha):
            angle_value = interpolate(0, 720, alpha)
            angle.set_value(angle_value)
            line1_end = circle.point_from_proportion(0.4 + alpha * 0.4)
            line1.put_start_and_end_on(circle.get_center(), line1_end)

        self.play(UpdateFromAlphaFunc(angle, update_angle_and_drag_line), run_time=3)

        self.wait()  # Wait for the scene to end


# Create and run the animation
anim = CircleChordAnimation()
anim.render()
