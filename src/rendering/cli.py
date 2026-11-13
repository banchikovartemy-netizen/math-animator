"""Render trusted repository scenes; problem text is inert UTF-8 data."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from dataclasses import asdict
from math_engine.checks import require_passed
from validation.video import PROFILES, validate_video

ROOT = Path(__file__).resolve().parents[2]

def artifact_module(path):
    spec = importlib.util.spec_from_file_location("reviewed_solution", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def render(job, mode="preview"):
    if not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", job):
        raise ValueError("Invalid job name")
    manifest = json.loads((ROOT / "examples" / f"{job}.json").read_text())
    scene = (ROOT / manifest["scene"]).resolve()
    solution_file = (ROOT / manifest["solution"]).resolve()
    if not scene.is_relative_to(ROOT / "scenes") or not solution_file.is_relative_to(ROOT / "examples"):
        raise ValueError("Artifact must be in repository scenes/examples")
    name = manifest["class"]
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", name):
        raise ValueError("Invalid class name")
    output = ROOT / "outputs" / job / mode
    output.mkdir(parents=True, exist_ok=True)
    report = {"job": job, "mode": mode, "status": "failed"}
    target = output / f"{job}.mp4"
    target.unlink(missing_ok=True)
    try:
        solution = artifact_module(solution_file).build_solution()
        report["solution"] = asdict(solution)
        require_passed(solution.checks)
        if not solution.checks:
            raise ValueError("Provide explicit mathematical checks or unverified Check records")
        (output / "solution.json").write_text(json.dumps(asdict(solution), ensure_ascii=False, indent=2))
        for tool in ("ffmpeg", "ffprobe", "latex", "dvisvgm"):
            if not shutil.which(tool): raise RuntimeError(f"Missing dependency: {tool}")
        w, h, fps = PROFILES[mode]
        env = dict(os.environ)
        env["PYTHONPATH"] = os.pathsep.join([str(ROOT / "src"), str(ROOT), env.get("PYTHONPATH", "")])
        command = [sys.executable, "-m", "manim", str(scene), name, "--renderer", "cairo", "--resolution", f"{w},{h}", "--fps", str(fps), "--format", "mp4", "--media_dir", str(output / "media"), "--output_file", job, "--disable_caching"]
        with (output / "render.log").open("w") as log:
            subprocess.run(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT, check=True, timeout=1800)
        candidates = list((output / "media" / "videos").rglob(f"{job}.mp4"))
        if len(candidates) != 1: raise RuntimeError("Expected exactly one completed video")
        shutil.copy2(candidates[0], target)
        report["video"] = validate_video(target, mode)
        report["status"] = "passed"
        print(target)
    except Exception as error:
        report["error"] = str(error)
        raise
    finally:
        (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job")
    parser.add_argument("--mode", choices=PROFILES, default="preview")
    args = parser.parse_args()
    render(args.job, args.mode)

if __name__ == "__main__": main()
