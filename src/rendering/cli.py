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

def render(job, mode="preview", **kwargs):
    from rendering.pipeline import render_job
    return render_job(job, mode, **kwargs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job")
    parser.add_argument("--mode", choices=PROFILES, default="preview")
    parser.add_argument("--workers",type=int,default=3)
    parser.add_argument("--segment")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--assemble-from", type=Path)
    args = parser.parse_args()
    render(args.job, args.mode, segment=args.segment, smoke=args.smoke, assemble_from=args.assemble_from, workers=args.workers)

if __name__ == "__main__": main()
