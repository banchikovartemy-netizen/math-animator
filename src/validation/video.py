import json
import subprocess
from pathlib import Path

PROFILES = {"preview": (1280, 720, 24), "final": (1920, 1080, 30)}

def validate_video(path, mode):
    path = Path(path)
    if not path.is_file() or path.stat().st_size == 0:
        raise ValueError("Video missing or empty")
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], check=True, capture_output=True, text=True)
    data = json.loads(probe.stdout)
    video = next(s for s in data["streams"] if s["codec_type"] == "video")
    w, h, fps = PROFILES[mode]
    n, d = map(int, video["avg_frame_rate"].split("/"))
    if (video["width"], video["height"], n/d) != (w, h, fps):
        raise ValueError("Unexpected resolution or frame rate")
    if video["codec_name"] != "h264" or float(data["format"]["duration"]) <= 0:
        raise ValueError("Invalid codec or duration")
    subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(path), "-f", "null", "-"], check=True, capture_output=True)
    return {"width": w, "height": h, "fps": fps, "codec": video["codec_name"], "duration": float(data["format"]["duration"]), "decoded": True}
