import json
from fractions import Fraction
import subprocess
from pathlib import Path

PROFILES = {"preview": (1280, 720, 24), "final": (1920, 1080, 30)}

def validate_frame_rate(average, nominal, expected):
    # Concatenating hundreds of Manim clips rounds timestamps to the MP4 clock.
    # Require the exact nominal rate and allow <0.0001 FPS metadata rounding.
    actual = Fraction(average)
    if Fraction(nominal) != expected or abs(actual - expected) > Fraction(1, 10000):
        raise ValueError("Unexpected frame rate")
    return float(actual)

def validate_video(path, mode):
    path = Path(path)
    if not path.is_file() or path.stat().st_size == 0:
        raise ValueError("Video missing or empty")
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], check=True, capture_output=True, text=True)
    data = json.loads(probe.stdout)
    video = next(s for s in data["streams"] if s["codec_type"] == "video")
    w, h, fps = PROFILES[mode]
    actual_fps = validate_frame_rate(video["avg_frame_rate"], video["r_frame_rate"], fps)
    if (video["width"], video["height"]) != (w, h):
        raise ValueError("Unexpected resolution")
    if video["codec_name"] != "h264" or float(data["format"]["duration"]) <= 0:
        raise ValueError("Invalid codec or duration")
    subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(path), "-f", "null", "-"], check=True, capture_output=True)
    return {"width": w, "height": h, "fps": fps, "average_fps": actual_fps, "codec": video["codec_name"], "duration": float(data["format"]["duration"]), "decoded": True}
