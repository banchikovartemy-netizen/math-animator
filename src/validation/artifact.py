"""Recheck an existing render without spending time rendering the scene again."""
import argparse
from dataclasses import asdict
import json
from pathlib import Path
import re
from math_engine.checks import require_passed
from rendering.cli import ROOT, artifact_module
from validation.video import validate_video


def verify_artifact(job, mode, directory):
    if not re.fullmatch(r'[a-z][a-z0-9_]{0,63}', job):
        raise ValueError('Invalid job')
    manifest = json.loads((ROOT / 'examples' / f'{job}.json').read_text())
    solution_path = (ROOT / manifest['solution']).resolve()
    if not solution_path.is_relative_to(ROOT / 'examples'):
        raise ValueError('Solution must be a trusted repository artifact')
    solution = artifact_module(solution_path).build_solution()
    require_passed(solution.checks)
    output = Path(directory) / job / mode
    report_path = output / 'report.json'
    report = json.loads(report_path.read_text())
    if (report['job'], report['mode'], report['solution']) != (job, mode, asdict(solution)):
        raise ValueError('Rendered solution does not match current checked mathematics')
    video = validate_video(output / f'{job}.mp4', mode)
    old_error = report.pop('error', None)
    if old_error:
        report['previous_validation_error'] = old_error
    report.update(status='passed', video=video, revalidated=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps(video, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('job')
    parser.add_argument('--mode', choices=['preview', 'final'], required=True)
    parser.add_argument('--directory', type=Path, required=True)
    args = parser.parse_args()
    verify_artifact(args.job, args.mode, args.directory)


if __name__ == '__main__':
    main()
