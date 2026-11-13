import pytest
from manim import Dot, RIGHT, tempconfig
from animation.components import ExplainedScene
from math_engine.checks import Check


def test_bounds_reject_offscreen_object():
    with tempconfig({"pixel_width": 1280, "pixel_height": 720, "frame_width": 14.222222, "frame_height": 8}):
        scene = ExplainedScene()
        scene.setup()
        scene.check_frame(Dot())
        with pytest.raises(ValueError, match="outside frame"):
            scene.check_frame(Dot().shift(RIGHT * 20))


def test_unknown_check_status_rejected():
    with pytest.raises(ValueError):
        Check("claim", "probably", "guess")
