from manim import *
import numpy as np

BACKGROUND = "#101827"
ACCENT = "#64D8CB"

class ExplainedScene(Scene):
    """Reusable layout primitives; individual scenes own their mathematics."""
    def setup(self):
        self.camera.background_color = BACKGROUND
        config.tex_template = TexTemplate(preamble=r"\usepackage{amsmath}\usepackage{amssymb}")
        self.caption = None
        self.layout_checks = 0

    def fit(self, obj, width=12.3, height=5.5):
        if obj.width > width: obj.scale_to_fit_width(width)
        if obj.height > height: obj.scale_to_fit_height(height)
        return obj

    def check_frame(self, *objects):
        for obj in objects:
            if (obj.get_left()[0] < -config.frame_width/2 + .12 or
                obj.get_right()[0] > config.frame_width/2 - .12 or
                obj.get_bottom()[1] < -config.frame_height/2 + .12 or
                obj.get_top()[1] > config.frame_height/2 - .12):
                raise ValueError(f"Object outside frame: {type(obj).__name__}")
            self.layout_checks += 1

    def heading(self, title):
        obj = self.fit(Text(title, font="DejaVu Sans", font_size=34), height=.55)
        obj.to_edge(UP, buff=.3)
        self.check_frame(obj)
        self.play(Write(obj))
        return obj

    def explain(self, text):
        obj = self.fit(Text(text, font="DejaVu Sans", font_size=25), width=12, height=.65)
        obj.to_edge(DOWN, buff=.32)
        self.check_frame(obj)
        if self.caption is None: self.play(FadeIn(obj, shift=UP*.15))
        else: self.play(ReplacementTransform(self.caption, obj))
        self.caption = obj
        self.wait(1.3)

    def formula(self, tex, y=0, color=WHITE):
        obj = self.fit(MathTex(tex, color=color), height=1.25).move_to(UP*y)
        self.check_frame(obj)
        return obj

    def transform_formula(self, old, tex, y=0):
        new = self.formula(tex, y)
        self.play(TransformMatchingTex(old, new))
        self.wait(.7)
        return new
