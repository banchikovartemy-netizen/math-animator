import json
import subprocess
import pytest
from rendering.cli import render
from validation.video import validate_video

@pytest.mark.parametrize("job", ["../bad", "x;echo hi", "", "a/b", "$(id)"])
def test_job_name_never_becomes_code(job):
    with pytest.raises(ValueError): render(job)

def test_missing_video(tmp_path):
    with pytest.raises(ValueError): validate_video(tmp_path / "absent.mp4", "preview")

def test_real_video_validation(tmp_path):
    path = tmp_path / "test.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=c=black:s=1280x720:r=24", "-t", "0.25", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(path)], check=True)
    assert validate_video(path, "preview")["decoded"]
    with pytest.raises(ValueError): validate_video(path, "final")

def test_truncated_video(tmp_path):
    path=tmp_path / "broken.mp4"
    path.write_bytes(b"not a video")
    with pytest.raises(subprocess.CalledProcessError): validate_video(path, "preview")
