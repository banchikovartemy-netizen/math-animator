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


def test_long_manim_movie_timestamp_rounding():
    from validation.video import validate_frame_rate
    # Observed in the real 547-animation matrix5 preview (9493 frames).
    assert abs(validate_frame_rate("854370000/35598743", "24/1", 24) - 24) < 0.0001
    for average, nominal in [("24000/1001", "24000/1001"), ("30/1", "30/1"), ("241/10", "24/1")]:
        with pytest.raises(ValueError): validate_frame_rate(average, nominal, 24)


def test_revalidate_keeps_video_and_rejects_changed_mathematics(tmp_path):
    from dataclasses import asdict
    from examples.matrix5_solution import build_solution
    from validation.artifact import verify_artifact
    directory = tmp_path / 'matrix5' / 'preview'
    directory.mkdir(parents=True)
    video = directory / 'matrix5.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'color=c=black:s=1280x720:r=24', '-t', '0.25', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(video)], check=True)
    original_bytes = video.read_bytes()
    report = {'job':'matrix5', 'mode':'preview', 'solution':asdict(build_solution()), 'status':'failed', 'error':'Unexpected frame rate'}
    path = directory / 'report.json'
    path.write_text(json.dumps(report))
    verify_artifact('matrix5', 'preview', tmp_path)
    updated = json.loads(path.read_text())
    assert updated['status'] == 'passed'
    assert updated['previous_validation_error'] == 'Unexpected frame rate'
    assert video.read_bytes() == original_bytes
    updated['solution']['goal'] = 'Changed mathematical problem'
    path.write_text(json.dumps(updated))
    with pytest.raises(ValueError, match='does not match'):
        verify_artifact('matrix5', 'preview', tmp_path)
