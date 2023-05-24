from manim import *

config.background_color = "#0c0b29"
config.pixel_height = 1080
config.pixel_width = 1920


class Chord(Scene):
    def form_chord(
        self,
        dr: float,
        dc: str,
        ts: float,
        cr: float,
        cc: str,
        op: np.ndarray,
        opdc: str,
        ar: float,
        ac: str,
    ):
        # all auxiliary functions
        def go_around_circle(mob, dt):
            """
            dt = difference (in seconds) since last frame. At 60fps render, this
            is equivalent to 1/60.

            The "nonlocal" keyword links offset to the variable initialized in
            form_chord(). It's not pretty (urgrgghh this is kind of global state
            grghrhgh) but because of the way add_updater is designed (limiting
            arguments solely to a Mobject and a dt variable which it
            automatically changes on its own somehow) this is my best option. My
            alternative would be to make offset an instance variable and call it
            over and over again but this would be grossly inefficient due to
            constant re-evaluation of self.offset at runtime. I would add a 3rd
            parameter to this function if I could, but...what can ya do
            """
            nonlocal circ_offset
            circ_offset += dt * ts
            pfp = circle.point_from_proportion(circ_offset % 1)
            if (pfp == ORIGIN).all():
                """
                There has to be a tiny offset to trav_dot's position whenever it
                gets to the origin to prevent mov_line and stat_line from ever
                being parallel so that the construction of the Angle object in
                get_angle() doesn't crap itself
                """
                pfp += origin_offset
            mob.move_to(pfp)

        def get_mov_line():
            return Line(op, trav_dot.get_center(), color=BLUE)

        def get_stat_line():
            return Line(trav_dot.get_center(), ORIGIN, color=ORANGE)

        def get_angle():
            return Angle(stat_line, mov_line, ar, color=ac)

        # "main" code!
        trav_dot = Dot(radius=dr, color=dc, fill_opacity=0.0)
        op_dot = Dot(radius=dr, color=opdc)
        circle = Circle(radius=cr, color=cc)
        stat_line = Line(op, ORIGIN, color=PURPLE)
        origin_offset = UP * 0.01
        circ_offset = 0

        """
        tiny initial position offset, for same reason as explained in
        go_around_circle(). Otherwise, the first frame can't render
        """
        trav_dot.move_to(ORIGIN + origin_offset)

        op_dot.move_to(op)
        circle.move_to(op)

        # init updater and redraw
        mov_line = always_redraw(get_mov_line)
        chord_line = always_redraw(get_stat_line)
        trav_dot.add_updater(go_around_circle)
        angol = always_redraw(get_angle)

        # add everything
        self.add(stat_line)
        self.add(circle)
        self.add(trav_dot)
        self.add(angol)
        self.add(mov_line)
        self.add(chord_line)
        self.add(op_dot)

        # can updater after sum secs
        self.wait(4)
        trav_dot.remove_updater(go_around_circle)

    def construct(self):
        self.form_chord(
            0.1,
            YELLOW,
            0.25,
            3.0,
            RED,
            np.array([-3, 0, 0]),
            WHITE,
            0.5,
            YELLOW,
        )
